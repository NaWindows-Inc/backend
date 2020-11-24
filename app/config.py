from os import getenv
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """
    Base environment configurations
    """
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", "NOT_FOUND")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv("SECRET_KEY", "NOT_FOUND")
    JWT_BLACKLIST_ENABLED1 = True
    FLASK_APP = 'run.py'


class Development(BaseConfig):
    """
    Development environment configurations
    """
    DEBUG = True
    TESTING = True
    ENV = 'development'


class Production(BaseConfig):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    ENV = 'production'