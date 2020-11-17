from app import db, ma
from datetime import datetime
from marshmallow import fields


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


    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<BLE Data id: {}, mac: {}>'.format(self.id, self.mac)


class BleDataSchema(ma.Schema):
    """
    Data from Ble scanner Schema for serializing
    """
    id = fields.Int()
    mac = fields.Str()
    level = fields.Int()
    time = fields.DateTime()
    

    class Meta:
        model = BleData
        field = ('id', 'mac', 'level', 'time')
        exclude = ('id',)
        