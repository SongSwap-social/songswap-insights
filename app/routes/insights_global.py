from flask import Blueprint, jsonify, request

from app.cache.decorators import cached
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
DEFAULT_LIMIT = 10


def get_limit_from_request() -> int:
    """
    Helper function to parse and validate the limit query parameter.

    Returns:
        int: The limit value parsed from the request query parameters.

    Raises:
        ValueError: If the limit query parameter is not between 1 and 100.
    """
    limit = request.args.get("limit")
    if limit:
        limit = int(limit)
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")
    else:
        limit = DEFAULT_LIMIT

    return limit


def get_top_items(getter: callable) -> tuple:
    """
    Given a getter function, returns a JSON response containing the top items (tracks or artists) based on the given getter function.
    NOTE: The getter function should take a limit as an argument and return a list of top items.

    Args:
        getter (callable): A callable that returns a list of top items.

    Returns:
        tuple: A JSON response containing the top items and a status code.

    Raises:
        ValueError: If the limit query parameter is not between 1 and 100.
    """
    try:
        limit = get_limit_from_request()
    except ValueError as e:
        # If the limit is not valid, return a JSON response with an error message and a 400 status code.
        return jsonify({"error": str(e)}), 400

    # Call the getter function with the given limit to get the top items.
    items = getter(limit)

    # Return a JSON response with the top items and a 200 status code.
    return jsonify(items), 200


# Function to get top tracks, given a user ID
# Example: http://songwap.social/insights/global/total/listens
@insights_global_bp.route("/total/listens", methods=["GET"])
@cached()
def total_listens():
    tracks = get_total_listens()
    return jsonify(tracks), 200


@insights_global_bp.route("/distinct/tracks", methods=["GET"])
@cached()
def distinct_tracks():
    tracks = get_distinct_tracks()
    return jsonify(tracks), 200


@insights_global_bp.route("/distinct/artists", methods=["GET"])
@cached()
def distinct_artists():
    artists = get_distinct_artists()
    return jsonify(artists), 200


@insights_global_bp.route("/distinct/primary-artists", methods=["GET"])
@cached()
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
@cached()
def top_tracks():
    return get_top_items(get_top_tracks)


# Function to get top artists
# Example: http://songwap.social/insights/global/top/artists?limit=10
@insights_global_bp.route("/top/artists", methods=["GET"])
@cached()
def top_artists():
    return get_top_items(get_top_artists)


# Function to get top primary artists
# Example: http://songwap.social/insights/global/top/primary-artists?limit=10
@insights_global_bp.route("/top/primary-artists", methods=["GET"])
@cached()
def top_primary_artists():
    return get_top_items(get_top_primary_artists)


# Function to get top listeners
# Example: http://songwap.social/insights/global/top/listeners?limit=10
@insights_global_bp.route("/top/listeners", methods=["GET"])
@cached()
def top_listeners():
    return get_top_items(get_top_listeners)
