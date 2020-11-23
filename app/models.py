from app import db
from datetime import datetime


class BleData(db.Model):
    """
    Data from BLE scanner Model
    """
    __tablename__ = 'ble_data'

    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, mac, level, time):
        self.mac = mac
        self.level = level
        self.time = time


    def __repr__(self):
        return '<BLE Data id: {}, mac: {}>'.format(self.id, self.mac)


class User(db.Model):
    """
    Data from user
    """
    __tablename__ = 'user_data'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(150))
    
    def __init__(self, public_id, username, password, email):
        self.public_id = public_id
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)