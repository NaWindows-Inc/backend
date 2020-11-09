from app import app
from models import BleData, BleDataSchema
from flask import request, jsonify, abort, make_response


bleDataSchemaOne = BleDataSchema()
bleDataSchemaAll = BleDataSchema(many=True)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/api/bledata', methods=['GET'])
def get_all_data():
    all_data = BleData.query.all()
    result = bleDataSchemaAll.dump(all_data)
    return jsonify(result)


@app.route('/api/bledata/<id>', methods=['GET'])
def get_one_data():
    one_data = BleData.query.get(id)
    result = bleDataSchemaOne.dump(one_data)
    return jsonify(result)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found page'}), 404)