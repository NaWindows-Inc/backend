from flask import Flask
from config import Development, Production

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

ma = Marshmallow(app)