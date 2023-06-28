from functools import wraps
from typing import Callable

from flask import current_app, request

from app import simple_cache


def cached(timeout: int = None, key_prefix: str = "", unless: Callable = None):
    """
    A decorator that caches the response of a Flask view function.

    This decorator wraps the Flask-Caching decorator and adds logging.

    Args:
        timeout (int, optional): The time in seconds for which the response should be cached.
            If None, the response is cached indefinitely. Defaults to None.
        key_prefix (str, optional): A string to prefix the cache key with. Defaults to "".
        unless (Callable, optional): A function that takes the Flask response object and returns
            True if the response should not be cached. Defaults to None.

    Returns:
        Callable: The decorated function.

    Example:
        @app.route('/my-route')
        @cached(timeout=60, key_prefix='my-route')
        def my_view_function():
            # ...
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create the cache key
            cache_key = key_prefix + request.full_path
            # e.g., /insights/top/tracks/1?limit=10
            # cache_key = request.full_path

            # Try to load the value from the cache
            rv = simple_cache.get(cache_key)
            # If cache hit, log and return the value
            if rv is not None:
                current_app.logger.info(f"Cache HIT: {cache_key}")
                return rv

            # If cache miss, log, call the function, store the result in cache, and return the value
            current_app.logger.info(f"Cache MISS: {cache_key}")
            rv = f(*args, **kwargs)

            # Cache the response
            if timeout:
                simple_cache.set(cache_key, rv, timeout=timeout)
            else:
                simple_cache.set(cache_key, rv)

            return rv

        return decorated_function

    return decorator
