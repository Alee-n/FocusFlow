from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
import csv
from flask import Response
from services.planner_service import generate_plan
from services.planner_service import format_duration
from database.db import get_session_chart_data
from database.db import save_session
from database.db import get_user_total_sessions
from database.db import get_user_sessions
from database.db import get_user_streak
from database.db import get_total_focus_time
from database.db import get_average_session_time
from database.db import get_most_common_energy
from database.db import get_most_used_mode

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():

    if "user" not in session:

        return redirect("/login")

    result = None

    username = session["user"]

    if request.method == "POST":

        task = request.form["task"]

        hours = int(request.form["hours"])

        minutes = int(request.form["minutes"])

        time = (hours * 60) + minutes

        energy = request.form["energy"]

        mode = request.form["mode"]

        result = generate_plan(task, time, energy, mode)

        try:

            save_session(username, task, time, energy, mode)

        except Exception as e:

            print("SAVE SESSION ERROR:", e)

            raise

    total = get_user_total_sessions(username)

    focus_time = get_total_focus_time(username)

    focus_time_display = format_duration(focus_time)

    average_time = get_average_session_time(username)

    average_time_display = format_duration(int(average_time))

    common_energy = get_most_common_energy(username)

    common_mode = get_most_used_mode(username)

    history = get_user_sessions(username)

    chart_data = get_session_chart_data(username)

    streak = get_user_streak(username)

    percent = 0

    return render_template(
        "index.html",
        result=result,
        total=total,
        percent=percent,
        history=history,
        chart_data=chart_data,
        username=username,
        streak=streak,
        focus_time=focus_time,
        focus_time_display=focus_time_display,
        average_time=average_time,
        average_time_display=average_time_display,
        common_energy=common_energy,
        common_mode=common_mode,
    )

@main.route("/export-csv")
def export_csv():

    username = session["user"]

    history = get_user_sessions(username)

    def generate():

        yield "Task,Minutes,Energy,Mode\n"

        for item in history:

            yield f"{item[0]},{item[1]},{item[2]},{item[3]}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=focusflow_history.csv"
        },
    )