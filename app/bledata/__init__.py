from flask import Blueprint

bledata = Blueprint('bledata', __name__)

from . import views