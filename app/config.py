import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


class BaseConfig:
    """
    Base environment configurations
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
    JWT_BLACKLIST_ENABLED = True
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