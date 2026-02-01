import sqlite3
from flask import Flask
from flask import render_template, request, redirect, flash

import db
import users

app = Flask(__name__)

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
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")