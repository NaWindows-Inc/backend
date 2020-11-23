from . import bledata
from app import db
from app.models import BleData
from app.schemes import BleDataSchema
from flask import request, jsonify
from sqlalchemy import func
from app.views import token_required


bleDataSchemaAll = BleDataSchema(many=True)
bleDataSchemaOne = BleDataSchema()


# get data /api/bledata/ - all data, /api/bledata/?count=NUM&page=NUM - get with pagination
@bledata.route('/', methods=['GET'])
@token_required
def get_one_page(current_user):
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


# upload data to db
@bledata.route('/upload', methods=['POST','GET'])
def add_one_data():
    # print(request.get_json())
    if request.method == 'POST':
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
    if request.method == 'GET':
        return jsonify({'error':'use POST request'})


# delete all data from db
@bledata.route('/delete')
@token_required
def delete_all_data(current_user):
    try:
        num_rows_deleted = db.session.query(BleData).delete()
        db.session.commit()
        return jsonify({"deleted":num_rows_deleted})
    except Exception as er:
        db.session.rollback()
        return jsonify({'error': str(er)})