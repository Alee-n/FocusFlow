def format_duration(total_minutes):

    hours = total_minutes // 60

    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} mins"

    if minutes == 0:
        return f"{hours} hr"

    return f"{hours} hr {minutes} mins"

def generate_plan(task, time, energy, mode):

    time = int(time)

    result = {}

    result["task"] = task.capitalize()

    result["score"] = "AI" if mode == "ai" else "Smart"

    # ---------- MOTIVATION ----------

    if energy == "low":
        motivation = "Start small. Even 5 minutes matters."

    elif energy == "medium":
        motivation = "Stay consistent. You're doing well."

    else:
        motivation = "You're in peak mode. Push hard!"

    result["motivation"] = motivation

    # ---------- ACTIVITY POOLS ----------

    study_activities = [
        "Deep Study",
        "Revision",
        "Practice Questions",
        "Recall Session",
        "Mock Test",
        "Problem Solving",
        "Concept Review",
        "Active Recall",
        "Previous Questions",
        "Topic Reinforcement"
    ]

    work_activities = [
        "Deep Work",
        "Planning",
        "Execution",
        "Review",
        "Optimization",
        "Documentation",
        "Research",
        "Implementation",
        "Testing",
        "Wrap Up"
    ]

    plan = []

    remaining = time

    index = 0

    if task == "study":

        activities = study_activities

    else:

        activities = work_activities

    # ---------- PLAN GENERATION ----------

    while remaining > 0:

        if energy == "low":
            focus_block = 20

        elif energy == "medium":
            focus_block = 25

        else:
            focus_block = 30

        session_time = min(focus_block, remaining)

        plan.append(
            f"{session_time} mins {activities[index % len(activities)]}"
        )

        remaining -= session_time

        if remaining >= 5:

            plan.append("5 mins Break")

            remaining -= 5

        index += 1

    result["plan"] = plan

    return result