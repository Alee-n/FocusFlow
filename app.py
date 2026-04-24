from flask import Flask, render_template, request

app = Flask(__name__)

def generate_plan(task, hours, energy):
    hours = float(hours)

    if energy == "low":
        focus = 20
        break_time = 10
        tip = "Start slow and build momentum."
    elif energy == "medium":
        focus = 30
        break_time = 5
        tip = "Maintain steady focus."
    else:
        focus = 45
        break_time = 10
        tip = "Deep work mode activated."

    total_minutes = hours * 60
    sessions = int(total_minutes // (focus + break_time))

    if sessions == 0:
        return f"Not enough time. Just do 1 quick {focus}-minute session."

    return (
        f"Task: {task}\n"
        f"Plan: {sessions} sessions of {focus} min focus + {break_time} min break.\n"
        f"Tip: {tip}"
    )

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""
    if request.method == "POST":
        task = request.form.get("task")
        hours = request.form.get("hours")
        energy = request.form.get("energy")

        output = generate_plan(task, hours, energy)

    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)