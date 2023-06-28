from app import create_app
from config import FLASK_RUN_PORT

app = create_app()

if __name__ == "__main__":
    app.run(port=FLASK_RUN_PORT)
