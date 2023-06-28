from flask import Blueprint, jsonify, request

from app.cache.decorators import cached
from app.services.insights_service import (
    get_top_artists,
    get_top_primary_artists,
    get_top_tracks,
)

insights_bp = Blueprint("insights", __name__, url_prefix="/insights")
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


def get_top_items(user_id: int, getter) -> tuple:
    """
    Given a user ID and a getter function, returns a tuple containing the top items (tracks or artists) for that user.

    Args:
        user_id (int): The ID of the user.
        getter (function): A function that takes a user ID and a limit and returns the top items for that user.

    Returns:
        tuple: A tuple containing the top items for the user and a status code.

    Raises:
        ValueError: If the limit query parameter is not between 1 and 100.
        ValueError: If the user_id parameter is not an integer.
    """
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user_id parameter"}), 400

    try:
        limit = get_limit_from_request()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    items = getter(user_id, limit)
    return jsonify(items), 200


# Function to get top tracks, given a user ID, optionally with a limit query parameter
# Example: http://songwap.social/insights/top-tracks/1?limit=10
@insights_bp.route("/top/tracks/<user_id>", methods=["GET"])
@cached()
def top_tracks(user_id):
    return get_top_items(user_id, get_top_tracks)


# Function to get top artists, given a user ID, optionally with a limit query parameter
# Example: http://songwap.social/insights/top-artists/1?limit=10
@insights_bp.route("/top/artists/<user_id>", methods=["GET"])
@cached()
def top_artists(user_id):
    return get_top_items(user_id, get_top_artists)


# Function to get top primary artists, given a user ID, optionally with a limit query parameter
# Example: http://songwap.social/insights/top-primary-artists/1?limit=10
@insights_bp.route("/top/primary-artists/<user_id>", methods=["GET"])
@cached()
def top_primary_artists(user_id):
    return get_top_items(user_id, get_top_primary_artists)
