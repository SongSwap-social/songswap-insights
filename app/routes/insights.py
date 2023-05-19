from flask import Blueprint, jsonify, request
from app.services.insights_service import get_top_tracks

insights_bp = Blueprint("insights", __name__)


@insights_bp.route("/top-tracks", methods=["GET"])
def top_tracks():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    tracks = get_top_tracks(user_id)
    return jsonify(tracks), 200
