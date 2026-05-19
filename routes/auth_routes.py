from flask import Blueprint, render_template, request, redirect, session

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from database.db import create_user, get_user

auth = Blueprint("auth", __name__)


# ---------- REGISTER ----------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        create_user(username, hashed_password)

        return redirect("/login")

    return render_template("register.html")


# ---------- LOGIN ----------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = get_user(username)

        if user and check_password_hash(user[2], password):

            session["user"] = username

            return redirect("/")

    return render_template("login.html")


# ---------- LOGOUT ----------
@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
