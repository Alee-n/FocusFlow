from flask import Blueprint, render_template, request, redirect, session

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from database.db import (create_user,get_user_by_username,get_user_by_email,)

auth = Blueprint("auth", __name__)


# ---------- REGISTER ----------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        existing_user = get_user_by_username(username)

        if existing_user:

            return "Username already exists"

        existing_email = get_user_by_email(email)

        if existing_email:

            return "Email already exists"

        create_user(username,email,hashed_password)

        return redirect("/login")

    return render_template("register.html")


# ---------- LOGIN ----------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = get_user_by_username(username)

        if user and check_password_hash(user[3], password):

            session["user"] = username

            return redirect("/")

    return render_template("login.html")


# ---------- LOGOUT ----------
@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
