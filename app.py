import sqlite3
import secrets
from flask import Flask
from flask import render_template, request, redirect, flash, session, abort

import db
import users
import events
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    events_list = events.get_events()
    return render_template("index.html", events=events_list)

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get("query")
    results = events.search(query) if query else events.get_events()
    return render_template("search.html", events=results, query=query)

@app.route("/my_events")
def my_events():
    user_id = session["user_id"]
    if not user_id:
        abort(404)
    organizing = events.get_events_by_organizer(user_id)
    attending = events.get_attending_events_for_user(user_id)
    return render_template("my_events.html", organizing=organizing, attending=attending)

@app.route("/new_event", methods=["GET", "POST"])
def new_event():
    if request.method == "GET":
        return render_template("new_event.html")

    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        location = request.form["location"]
        description = request.form["description"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        user_id = session["user_id"]

        event_id = events.add_event(
                            title, location, description,
                            start_time, end_time, user_id)
        return redirect("/event/" + str(event_id))

@app.route("/event/<int:event_id>")
def event(event_id):
    event = events.get_event(event_id)
    if not event:
        abort(404)
    organizer = users.get_user(event["user_id"])
    rsvp = events.get_rsvp(event["user_id"], session["user_id"])
    attendees = events.get_attendees_by_event(event_id)
    snacks = events.get_snacks_by_event(event_id)
    diets = events.get_diets_by_event(event_id)
    responses = events.get_rsvps_by_event(event_id)
    return render_template("event.html",
        event=event, organizer=organizer,
        rsvp=rsvp, attendees=attendees,
        snacks=snacks, diets=diets, responses=responses)
    

@app.route("/delete_event/<int:event_id>", methods=["GET", "POST"])
def remove_event(event_id):
    event = events.get_event(event_id)
    if not event:
        abort(404)
    if event["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_event.html", event=event)

    if request.method == "POST":
        check_csrf()
        if "delete" in request.form:
            events.delete_event(event_id)
            return redirect("/")
        else:
            return redirect("/event/" + str(event_id))

@app.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    event = events.get_event(event_id)
    if not event:
        abort(404)
    if event["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_event.html", event=event)

    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        events.update_event(
            event_id, 
            title=request.form["title"],
            location=request.form["location"],
        )

        return redirect("/event/" + str(event_id))

@app.route("/new_rsvp", methods=["POST"])
def new_rsvp():
    check_csrf()

    status = request.form["status"]
    diet = request.form["diet"]
    snack = request.form["snack"]
    greetings = request.form["greetings"]
    event_id = request.form["event_id"]
    user_id = session["user_id"]

    events.add_rsvp(status, diet, snack, greetings, event_id, user_id)

    return redirect("/event/" + str(event_id))

@app.route("/user/<int:user_id>")
def user(user_id):
    user = users.get_user(user_id)
    organizing = events.get_events_by_organizer(user_id)
    attending = events.get_attending_events_for_user(user_id)
    if not user:
        abort(404)
    return render_template("user.html", user=user, organizing=organizing, attending=attending)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/createuser", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("error: passwords do not match")
        return redirect("/register")

    try:
        users.create_user(username, password1)
        user_id = users.validate_password(username, password=password1)
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    except sqlite3.IntegrityError:
        flash("error: the username is already reserved")
        return redirect("/register")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.validate_password(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("error: wrong username or password")
            return redirect("/login")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)