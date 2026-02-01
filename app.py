import sqlite3
from flask import Flask
from flask import render_template, request, redirect, flash, session

import db
import users
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    events = db.query("SELECT * FROM events")
    return render_template("index.html", events=events)

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
        return redirect("/")
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
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
            return redirect("/")
        else:
            flash("error: wrong username or password")
            return redirect("/login")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")