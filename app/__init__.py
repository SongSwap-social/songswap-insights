from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(
        "config"
    )  # ensure you have a `config.py` file in the root folder
    db.init_app(app)

    from app.routes.insights import insights_bp
    from app.routes.insights_global import insights_global_bp

    app.register_blueprint(insights_bp, url_prefix="/insights")
    app.register_blueprint(insights_global_bp, url_prefix="/insights/global")

    return app
