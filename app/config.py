from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Configuration(object):
    DEBUG = True
    ENV = '.env'
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI", "NOT_FOUND")
    SQLALCHEMY_TRACK_MODIFICATIONS = False