from functools import lru_cache

from flask import Blueprint, jsonify, request

from app.services.insights_global_service import (
    get_distinct_artists,
    get_distinct_primary_artists,
    get_distinct_tracks,
    get_top_artists,
    get_top_listeners,
    get_top_primary_artists,
    get_top_tracks,
    get_total_listen_time,
    get_total_listens,
)

insights_global_bp = Blueprint(
    "insights_global", __name__, url_prefix="/insights/global"
)


# Function to get top tracks, given a user ID
# Example: http://songwap.social/insights/global/total/listens
@insights_global_bp.route("/total/listens", methods=["GET"])
@lru_cache(maxsize=1)
def total_listens():
    tracks = get_total_listens()
    return jsonify(tracks), 200


@insights_global_bp.route("/distinct/tracks", methods=["GET"])
@lru_cache(maxsize=1)
def distinct_tracks():
    tracks = get_distinct_tracks()
    return jsonify(tracks), 200


@insights_global_bp.route("/distinct/artists", methods=["GET"])
@lru_cache(maxsize=1)
def distinct_artists():
    artists = get_distinct_artists()
    return jsonify(artists), 200


@insights_global_bp.route("/distinct/primary-artists", methods=["GET"])
@lru_cache(maxsize=1)
def distinct_primary_artists():
    artists = get_distinct_primary_artists()
    return jsonify(artists), 200


@insights_global_bp.route("/total/listen-time", methods=["GET"])
def total_listen_time(as_string: bool = False):
    listen_time = get_total_listen_time()

    as_string = request.args.get("as_string")
    if as_string:
        # Convert ms to human-readable format: {days}d {hours}h {minutes}m {seconds}s
        seconds = listen_time // 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        listen_time = f"{days}d {hours}h {minutes}m {seconds}s"
    return jsonify(listen_time), 200


# Function to get top tracks
# Example: http://songwap.social/insights/global/top/tracks?limit=10
@insights_global_bp.route("/top/tracks", methods=["GET"])
@lru_cache(maxsize=1)
def top_tracks(limit: int = 10):
    limit = request.args.get("limit")
    if limit:
        # Try converting to int
        try:
            limit = int(limit)
            if limit < 1 or limit > 100:
                return jsonify({"error": "Limit must be between 1 and 100"}), 400
        except ValueError:
            return jsonify({"error": "Invalid limit parameter"}), 400

    tracks = get_top_tracks(limit)
    return jsonify(tracks), 200


# Function to get top artists
# Example: http://songwap.social/insights/global/top/artists?limit=10
@insights_global_bp.route("/top/artists", methods=["GET"])
@lru_cache(maxsize=1)
def top_artists(limit: int = 10):
    limit = request.args.get("limit")
    if limit:
        # Try converting to int
        try:
            limit = int(limit)
            if limit < 1 or limit > 100:
                return jsonify({"error": "Limit must be between 1 and 100"}), 400
        except ValueError:
            return jsonify({"error": "Invalid limit parameter"}), 400

    artists = get_top_artists(limit)
    return jsonify(artists), 200


# Function to get top primary artists
# Example: http://songwap.social/insights/global/top/primary-artists?limit=10
@insights_global_bp.route("/top/primary-artists", methods=["GET"])
@lru_cache(maxsize=1)
def top_primary_artists(limit: int = 10):
    limit = request.args.get("limit")
    if limit:
        # Try converting to int
        try:
            limit = int(limit)
            if limit < 1 or limit > 100:
                return jsonify({"error": "Limit must be between 1 and 100"}), 400
        except ValueError:
            return jsonify({"error": "Invalid limit parameter"}), 400

    artists = get_top_primary_artists(limit)
    return jsonify(artists), 200


# Function to get top listeners
# Example: http://songwap.social/insights/global/top/listeners?limit=10
@insights_global_bp.route("/top/listeners", methods=["GET"])
@lru_cache(maxsize=1)
def top_listeners(limit: int = 10):
    limit = request.args.get("limit")
    if limit:
        # Try converting to int
        try:
            limit = int(limit)
            if limit < 1 or limit > 100:
                return jsonify({"error": "Limit must be between 1 and 100"}), 400
        except ValueError:
            return jsonify({"error": "Invalid limit parameter"}), 400

    listeners = get_top_listeners(limit)
    return jsonify(listeners), 200
