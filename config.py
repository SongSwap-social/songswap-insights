from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


DEBUG = environ.get("DEBUG", False)
SECRET_KEY = environ.get("SECRET_KEY")
FLASK_RUN_PORT = environ.get("FLASK_RUN_PORT", 5001)
SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False

CACHE_TYPE = environ.get("CACHE_TYPE", "SimpleCache")
CACHE_DEFAULT_TIMEOUT = int(environ.get("CACHE_DEFAULT_TIMEOUT", 300))
CACHE_CONFIG = {
    "DEBUG": DEBUG,
    "CACHE_TYPE": CACHE_TYPE,
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT,
}
