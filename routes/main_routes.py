from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect

from services.planner_service import generate_plan

from database.db import save_session
from database.db import get_user_total_sessions
from database.db import get_user_sessions

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():

    if "user" not in session:

        return redirect("/login")

    result = None

    username = session["user"]

    if request.method == "POST":

        task = request.form["task"]

        time = request.form["time"]

        energy = request.form["energy"]

        mode = request.form["mode"]

        result = generate_plan(task, time, energy, mode)

        save_session(username, task, time, energy, mode)

    total = get_user_total_sessions(username)

    history = get_user_sessions(username)

    percent = 0

    return render_template(
        "index.html",
        result=result,
        total=total,
        percent=percent,
        history=history,
        username=username,
    )
