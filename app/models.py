from app import db, ma
from datetime import datetime


class BleData(db.Model):
    """
    Data from BLE scanner Model
    """

    # table name
    __tablename__ = 'ble_data'


    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())
    page = db.Column(db.Integer, nullable=False)


    # def __init__(self, *args, **kwargs):
    #     super(BleData, self).__init__(*args, **kwargs)

    def __init__(self, mac, level, time, page):
        self.mac = mac
        self.level = level
        self.time = time
        self.page = page


    def save(self):
        db.session.add(self)
        db.session.commit()

    # def __repr__(self):
    #     return '<BLE Data id: {}, mac: {}>'.format(self.id, self.mac)


class BleDataSchema(ma.Schema):
    class Meta:
        model = BleData
        field = ('id', 'mac', 'level', 'time', 'page')
        