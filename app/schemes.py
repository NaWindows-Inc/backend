from app import ma
from marshmallow import fields
from app.models import BleData


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