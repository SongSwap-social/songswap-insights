from flask import Blueprint, jsonify, request

from app import simple_cache

cache_bp = Blueprint("cache", __name__, url_prefix="/cache")


@cache_bp.route("/invalidate", methods=["POST"])
def invalidate_cache():
    # Require a secret key to invalidate the cache
    secret_key = request.headers.get("X-Invalidation-Secret")
    if not secret_key or secret_key != "lol!this-is-THE-secret-key!123":
        # Return unauthorized if the secret key is missing or incorrect
        return jsonify({"error": "Invalid secret key"}), 403
    simple_cache.clear()
    return jsonify({"status": "success", "message": "Cache has been cleared"}), 200


@cache_bp.route("/size", methods=["GET"])
def cache_size():
    size = len(simple_cache.cache._cache.items())
    return jsonify({"size": size}), 200
