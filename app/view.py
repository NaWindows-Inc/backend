from app import app, db
from models import BleData, BleDataSchema
from flask import request, jsonify, abort, make_response
from sqlalchemy import func


bleDataSchemaAll = BleDataSchema(many=True)
bleDataSchemaOne = BleDataSchema()


@app.route('/hello')
def index():
    return 'Hello world'


@app.route('/api/bledata/', methods=['GET'])
def get_one_page():
    error = None
    try:
        num_page = int(request.args['page'])
        count_data = int(request.args['count'])
    except:
        num_page = 0
        count_data = 0

    if num_page and count_data:
        try:
            data_page = BleData.query.order_by(BleData.id.desc()).paginate(num_page,count_data,error_out=False)
            data_page_dump = bleDataSchemaAll.dump(data_page.items)
        except Exception as er:
            error = er

        if data_page_dump:
            totalCount = db.session.query(func.count(BleData.id)).scalar()
            result = {'items':data_page_dump, 'totalCount':totalCount, 'error': error}
            return jsonify(result)
        else:
            return not_found(error)
    else:
        all_data = BleData.query.order_by(BleData.id.desc()).all()
        all_data_dump = bleDataSchemaAll.dump(all_data)
        totalCount = db.session.query(func.count(BleData.id)).scalar()
        result = {'items':all_data_dump, 'totalCount':totalCount, 'error': error}
        return jsonify(result)


@app.route('/api/bledata/upload/', methods=['POST'])
def add_one_data():
    try:
        mac = request.json['mac']
        level = int(request.json['level'])
        time = request.json['time']

        new_data = BleData(mac, level, time)
        db.session.add(new_data)
        db.session.commit()

        return bleDataSchemaOne.jsonify(new_data)

    except Exception as er:
        return jsonify({'error':'wrong data format', 'wrong': str(er)})


@app.route('/api/bledata/delete/')
def delete_all_data():
    try:
        num_rows_deleted = db.session.query(BleData).delete()
        db.session.commit()
        return jsonify({"deleted":num_rows_deleted})
    except Exception as er:
        db.session.rollback()
        return jsonify({'error': str(er)})
    

@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return make_response(jsonify({'error':'not found page', 'description':str(error)}), 404)