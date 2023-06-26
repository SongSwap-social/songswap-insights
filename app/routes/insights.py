from functools import lru_cache
from flask import Blueprint, jsonify, request

from app.services.insights_service import (
    get_top_artists,
    get_top_primary_artists,
    get_top_tracks,
)

insights_bp = Blueprint("insights", __name__, url_prefix="/insights")


# Function to get top tracks, given a user ID
# Example: http://songwap.social/insights/top-tracks?user_id=1
@insights_bp.route("/top-tracks", methods=["GET"])
@lru_cache(maxsize=10)
def top_tracks():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    limit = request.args.get("limit")
    if limit:
        # Try converting to int
        try:
            limit = int(limit)
            if limit < 1 or limit > 100:
                return jsonify({"error": "Limit must be between 1 and 100"}), 400
        except ValueError:
            return jsonify({"error": "Invalid limit parameter"}), 400

    tracks = get_top_tracks(user_id, limit)
    return jsonify(tracks), 200


# Function to get top artists, given a user ID
# Example: http://songwap.social/insights/top-artists?user_id=1
@insights_bp.route("/top-artists", methods=["GET"])
@lru_cache(maxsize=10)
def top_artists():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    artists = get_top_artists(user_id)
    return jsonify(artists), 200


# Function to get top primary artists, given a user ID
# Example: http://songwap.social/insights/top-primary-artists?user_id=1
@insights_bp.route("/top-primary-artists", methods=["GET"])
@lru_cache(maxsize=10)
def top_primary_artists():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    artists = get_top_primary_artists(user_id)
    return jsonify(artists), 200
