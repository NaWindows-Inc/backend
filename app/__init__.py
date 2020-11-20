from flask import Flask
from app.config import Development, Production
import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(Development)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

ma = Marshmallow(app)
CORS(app)

from app import views


@app.before_first_request
def setup():
    db.create_all()