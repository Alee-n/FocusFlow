from flask import Blueprint, jsonify, request
from services.planner_service import generate_plan
from database.db import save_session

api = Blueprint("api", __name__)


@api.route("/api/health")
def health_check():

    return jsonify({"status": "running", "message": "FocusFlow API is working"})


@api.route("/api/generate-plan", methods=["POST"])
def api_generate_plan():

    data = request.get_json()

    task = data.get("task")
    time = int(data.get("time"))
    energy = data.get("energy")
    mode = data.get("mode")

    result = generate_plan(task, time, energy, mode)

    save_session("api_user", task, time, energy, mode)

    return jsonify({"success": True, "data": result})
