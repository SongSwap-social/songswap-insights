from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

from config import CACHE_CONFIG

db = SQLAlchemy()
simple_cache = Cache(config=CACHE_CONFIG)


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    simple_cache.init_app(app)

    from app.routes.cache import cache_bp
    from app.routes.insights import insights_bp
    from app.routes.insights_global import insights_global_bp

    app.register_blueprint(insights_bp)
    app.register_blueprint(insights_global_bp)
    app.register_blueprint(cache_bp)

    return app
