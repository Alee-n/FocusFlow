def generate_plan(task, time, energy, mode):

    time = int(time)

    result = {}

    result["task"] = task.capitalize()

    if mode == "ai":
        result["score"] = "AI"

    else:
        result["score"] = "Smart"

    # ---------- MOTIVATION ----------
    if energy == "low":
        motivation = "Start small. Even 5 minutes matters."

    elif energy == "medium":
        motivation = "Stay consistent. You're doing well."

    else:
        motivation = "You're in peak mode. Push hard!"

    result["motivation"] = motivation

    # ---------- PLAN GENERATION ----------
    plan = []

    if task == "study":

        if time >= 120:

            plan = [
                "25 mins Deep Study",
                "5 mins Break",
                "25 mins Revision",
                "10 mins Practice Questions",
                "20 mins Recall Session",
                "5 mins Break",
                "30 mins Mock Test",
            ]

        elif time >= 60:

            plan = ["25 mins Study", "5 mins Break", "25 mins Revision"]

        else:

            plan = ["20 mins Focus Study", "5 mins Quick Revision"]

    else:

        if time >= 120:

            plan = [
                "30 mins Deep Work",
                "10 mins Planning",
                "30 mins Execution",
                "10 mins Review",
                "20 mins Optimization",
            ]

        elif time >= 60:

            plan = ["25 mins Work Sprint", "5 mins Break", "25 mins Task Completion"]

        else:

            plan = ["20 mins Focus Work", "10 mins Wrap Up"]

    result["plan"] = plan

    return result
