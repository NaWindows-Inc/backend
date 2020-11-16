from app import app, db
from models import BleData, BleDataSchema
from flask import request, jsonify, abort, make_response
from sqlalchemy import func



bleDataSchemaAll = BleDataSchema(many=True)
bleDataSchemaOne = BleDataSchema()


@app.route('/hello')
def index():
    return 'Hello world'


@app.route('/api/bledata/all/', methods=['GET'])
def get_all_data():
    all_data = BleData.query.all()
    result = bleDataSchemaAll.dump(all_data)
    return jsonify(result)


@app.route('/api/bledata/', methods=['GET'])
def get_one_page():
    data_page_dump={}
    error = None
    try:
        data_page = BleData.query.filter(BleData.page == request.args['page'])
        data_page_dump = bleDataSchemaAll.dump(data_page)
    except Exception as er:
        error = er

    if data_page_dump:
        totalCount = db.session.query(func.max(BleData.page)).scalar()
        result = {'items':data_page_dump, 'totalCount':totalCount, 'error': error}
        return jsonify(result)
    else:
        return not_found(error)


@app.route('/api/bledata/upload/', methods=['POST'])
def add_one_data():
    mac = request.json['mac']
    level = request.json['level']
    time = request.json['time']

    totalCount = db.session.query(func.max(BleData.page)).scalar()
    data_page = BleData.query.filter(BleData.page == totalCount)
    data_page_dump = bleDataSchemaAll.dump(data_page)
    if len(data_page_dump) < 10:
        page = totalCount
    else:
        page = totalCount + 1
     
    new_data = BleData(mac, level, time, page)
    db.session.add(new_data)
    db.session.commit()

    return bleDataSchemaOne.jsonify(new_data)


@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return make_response(jsonify({'error':'Not found page', 'description':str(error)}), 404)