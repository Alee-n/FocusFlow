from flask import Blueprint, jsonify, request
from services.planner_service import generate_plan
from database.db import save_session, get_total_sessions
from flask_jwt_extended import (
create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

api = Blueprint("api", __name__)


@api.route("/api/health")
def health_check():

    return jsonify({"status": "running", "message": "FocusFlow API is working"})


@api.route("/api/generate-plan", methods=["POST"])
def api_generate_plan():

    data = request.get_json()

    if not data:

        return jsonify({"success": False, "error": "No JSON data provided"}), 400

    task = data.get("task")
    time = data.get("time")
    energy = data.get("energy")
    mode = data.get("mode")

    if not all([task, time, energy, mode]):

        return jsonify({"success": False, "error": "Missing required fields"}), 400

    try:

        time = int(time)

    except ValueError:

        return jsonify({"success": False, "error": "Time must be an integer"}), 400

    result = generate_plan(task, time, energy, mode)

    save_session("api_user", task, time, energy, mode)

    return jsonify({"success": True, "data": result})


@api.route("/api/history", methods=["GET"])
@jwt_required()
def history():

    current_user = get_jwt_identity()

    total = get_total_sessions()

    return jsonify({"user": current_user, "total_sessions": total})


@api.route("/api/add", methods=["POST"])
def add_session():

    data = request.get_json()

    task = data.get("task")
    time = data.get("time")
    energy = data.get("energy")
    mode = data.get("mode")

    save_session("api_user", task, time, energy, mode)

    return jsonify({"message": "Session saved successfully"})


@api.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")

    if not username:

        return jsonify({"success": False, "error": "Username required"}), 400

    role = "admin" if username == "admin" else "user"

    access_token = create_access_token(
        identity=username,
        additional_claims={
            "role": role
        }
    )

    return jsonify({"success": True, "access_token": access_token})


@api.route("/api/admin", methods=["GET"])
@jwt_required()
def admin_route():

    current_user = get_jwt_identity()

    claims = get_jwt()

    if claims["role"] != "admin":

        return jsonify({"success": False, "error": "Admin access required"}), 403

    return jsonify({"success": True, "message": "Welcome Admin", "user": current_user})
