from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(
        "config"
    )  # ensure you have a `config.py` file in the root folder
    db.init_app(app)

    return app
