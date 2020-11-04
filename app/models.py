from app import db
from datetime import datetime

class BleData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(17))
    level = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime.now())

    page = db.Column(db.Integer)


    def __init__(self, *args, **kwargs):
        super(BleData, self).__init__(*args, **kwargs)


    def __repr__(self):
        return '<BLE Data id: {}, mac: {}>'.format(self.id, self.mac)
        