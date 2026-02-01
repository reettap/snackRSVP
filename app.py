from flask import Flask
from flask import render_template
import db

app = Flask(__name__)

@app.route("/")
def index():
    events = db.query("SELECT * FROM events")
    return render_template("index.html", events=events)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")