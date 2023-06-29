from app import create_app
from config import DEBUG, FLASK_RUN_PORT


if __name__ == "__main__":
    app = create_app()
    app.run(port=FLASK_RUN_PORT, debug=DEBUG)
