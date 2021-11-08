"""Flask config."""
from os import environ, path

from decouple import config

BASE_DIR = path.abspath(path.dirname(__file__))


class Config:
    """Flask configuration variables."""

    # General Config
    FLASK_APP = config("FLASK_APP")
    FLASK_ENV = config("FLASK_ENV")
    SECRET_KEY = config("SECRET_KEY")

    # Assets
    LESS_BIN = config("LESS_BIN")
    ASSETS_DEBUG = config("ASSETS_DEBUG")
    LESS_RUN_IN_DEBUG = config("LESS_RUN_IN_DEBUG")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = config("COMPRESSOR_DEBUG")