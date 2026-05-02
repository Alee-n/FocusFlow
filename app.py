from flask import Flask, render_template, request, redirect, session
from google import genai
import sqlite3

# 👉 put your key here for now
client = genai.Client(api_key="YOUR_API_KEY")

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ---------------- #
def init_db():
    conn = sqlite3.connect("focusflow.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS progress(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        task TEXT,
        energy TEXT,
        completed INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- AI ---------------- #
def generate_ai_plan(task, time, energy):
    try:
        prompt = f"""
        Create a productivity plan.

        Task: {task}
        Time: {time} minutes
        Energy: {energy}

        Return bullet points.
        """

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except:
        return None

# ---------------- SMART PLAN ---------------- #
def generate_plan(task, time, energy):
    total = float(time)

    if energy == "low":
        focus, break_t = 20, 10
        score = 60
    elif energy == "medium":
        focus, break_t = 30, 5
        score = 75
    else:
        focus, break_t = 45, 10
        score = 90

    plan = []
    while total > focus:
        plan.append(f"Focus {focus} min → Break {break_t} min")
        total -= (focus + break_t)

    if total > 0:
        plan.append(f"Final {int(total)} min focus")

    return {
        "task": task,
        "score": score,
        "plan": plan
    }

# ---------------- ANALYTICS ---------------- #
def get_stats(user):
    conn = sqlite3.connect("focusflow.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM progress WHERE username=?", (user,))
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM progress WHERE username=? AND completed=1", (user,))
    done = c.fetchone()[0]

    conn.close()

    percent = int((done / total) * 100) if total > 0 else 0
    return total, percent

# ---------------- LOGIN ---------------- #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")

        conn = sqlite3.connect("focusflow.db")
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users(username) VALUES(?)", (user,))
        conn.commit()
        conn.close()

        session["user"] = user
        return redirect("/")

    return render_template("login.html")

# ---------------- MAIN ---------------- #
@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    result = None
    total, percent = get_stats(session["user"])

    if request.method == "POST":
        task = request.form.get("task")
        time = request.form.get("time")
        energy = request.form.get("energy")
        mode = request.form.get("mode")

        # save session
        conn = sqlite3.connect("focusflow.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO progress(username, task, energy, completed) VALUES(?,?,?,0)",
            (session["user"], task, energy)
        )
        conn.commit()
        conn.close()

        if mode == "ai":
            ai = generate_ai_plan(task, time, energy)
            if ai:
                result = {
                    "task": task,
                    "score": "AI",
                    "plan": ai.split("\n")
                }
            else:
                result = generate_plan(task, time, energy)
        else:
            result = generate_plan(task, time, energy)

    return render_template("index.html",
                           result=result,
                           total=total,
                           percent=percent)

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)