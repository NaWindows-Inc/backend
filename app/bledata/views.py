from . import bledata
from app import db
from app.models import BleData
from app.schemes import BleDataSchema
from flask import request, jsonify
from app.views import token_required
from app.db_operation import create, read, delete


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
            data_page = read(count=count_data, page=num_page)
            data_page_dump = bleDataSchemaAll.dump(data_page.items)
        except Exception as er:
            error = er

        if data_page_dump:
            totalCount = read()
            result = {'items':data_page_dump, 'totalCount':totalCount, 'error': error}
            return jsonify(result)
        else:
            return jsonify({'error':'Wrong page or count'})
    else:
        all_data = read(all_data=True)
        all_data_dump = bleDataSchemaAll.dump(all_data)
        totalCount = read()
        result = {'items':all_data_dump, 'totalCount':totalCount, 'error': error}
        return jsonify(result)


# upload data to db
@bledata.route('/upload', methods=['POST','GET'])
def add_one_data():
    print(str(request.json['mac'])+ '  '+str(request.json['level'])+'  '+str(request.json['time']))
    if request.method == 'POST':
        try:
            mac = request.json['mac']
            level = int(request.json['level'])
            time = request.json['time']

            new_data = BleData(mac, level, time)
            create(new_data=new_data)

            return bleDataSchemaOne.jsonify(new_data)
        except Exception:
            return jsonify({'error':'Wrong data format'})
    if request.method == 'GET':
        return jsonify({'error':'use POST request'})


# delete all data from db
@bledata.route('/delete', methods=['DELETE'])
@token_required
def delete_all_data(current_user):
    num_rows_deleted = delete(bledata=True)
    if num_rows_deleted:
        return jsonify({'deleted':num_rows_deleted, 'error': None})
    else:
        return jsonify({'error':'Nothing deleted'})