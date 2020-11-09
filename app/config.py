from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Development(object):
    """
    Development environment configurations
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", "NOT_FOUND")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'development'
    FLASK_APP = 'main.py'


class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', "NOT_FOUND")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'production'
    FLASK_APP = 'main.py'