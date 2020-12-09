from flask import Flask
from app.config import Development, Production

from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)

ma = Marshmallow(app)
CORS(app)


# Import the application views
from app import views

# register blueprints
from .users import users
app.register_blueprint(users, url_prefix='/user')

from .bledata import bledata
app.register_blueprint(bledata, url_prefix='/api/bledata')