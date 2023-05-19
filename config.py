from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
