from datetime import timedelta
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONES"] = False
app.secret_key = "asdfgfdsqwergfdstrewrtyurtyu"
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class User(db.Model):
    #__tablename__ = "Users"
    _id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    department = db.Column(db.String(20))
    role = db.Column(db.String(20))
    email = db.Column(db.String(20))

    def __init__(self, name, lname, department, role, email):
        self.name = name
        self.lname = lname
        self.department = department
        self.role = role
        self.email = email

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/user/list")
def list():
    users = User.query.all()
    return render_template("user_admin/list.html", users=users)

@app.route("/user/register", methods=("GET","POST"))
def register():
    if request.method == "POST":
        name = request.form["name"]
        lname = request.form["lname"]
        depart = request.form["department"]
        role = request.form["role"]
        email = request.form["email"]
        if not name or not lname or not depart or not role or not email:
            flash("There is missing data!")
        else:
            user = User(name, lname, depart, role, email)
            db.session.add(user)
            db.session.commit()
            flash('User added to database')
    return render_template("user_admin/register.html")

with app.app_context():
    db.create_all()