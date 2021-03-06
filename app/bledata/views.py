from . import bledata
from app import db
from app.models import BleData
from app.schemes import BleDataSchema
from flask import request, jsonify
from app.views import token_required
from app.db_operation import create, read, delete
import re


bleDataSchemaAll = BleDataSchema(many=True)
bleDataSchemaOne = BleDataSchema()


# get data /api/bledata/ - all data, 
# /api/bledata/?count=NUM&page=NUM - get with pagination
# /api/bledata/ with 'mac' in body - get all data by mac
@bledata.route('/', methods=['GET', 'POST'])
@token_required
def get_one_page(current_user):
    error = None
    if request.method == 'GET':
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
                return jsonify({'error':'Wrong page or count'}), 403
        else:
            all_data = read(all_data=True)
            all_data_dump = bleDataSchemaAll.dump(all_data)
            totalCount = read()
            result = {'items':all_data_dump, 'totalCount':totalCount, 'error': error}
            return jsonify(result)
    elif request.method == 'POST':
        try:
            data_mac = request.get_json()
            mac = data_mac.get('mac') 
        except:
            return jsonify({'error': 'Missing header', 'response':None}), 401
        
        if mac:
            if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
                all_data_mac = bleDataSchemaAll.dump(read(mac=mac))
                result = []
                for mac in all_data_mac:
                    result.append({
                        'level': mac['level'],
                        'time': mac['time'],
                    })
                return jsonify({'items': result, 'error': None, 'totalCount': len(all_data_mac)}) 
            else:
                return jsonify({'error':'Wrong mac format'}), 403
        
            
# upload data to db
@bledata.route('/upload', methods=['POST'])
def add_one_data():
    try:
        data = request.json
    except:
        try:
            data = request.get_json()
        except:
            data = ''
    if data: 
        try:
            mac, level, time = data.get('mac'), int(data.get('level')), data.get('time') 
        except Exception:
            return jsonify({'error':'Wrong data format'}), 403 

        try:
            response = upload_to_db(mac=mac, level=level, time=time)
        except:
            response = -2

        if response != -1 and response != -2 :
            print(str(mac)+ '  '+str(level)+'  '+str(time))
            return response
        elif response == -2:
            return jsonify({'error':'Wrong time format'}), 403
        else:
            return jsonify({'error':'Wrong mac format'}), 403
    else:
        try:
            mac, time, level = request.json['mac'], request.json['time'], int(request.json['level'])
            
            response = upload_to_db(mac=mac, level=level, time=time)
            if response != -1:
                print(str(mac)+ '  '+str(level)+'  '+str(time))
                return response
            else:
                return jsonify({'error':'Wrong mac format'}), 403 
        except Exception:
            return jsonify({'error':'Wrong data format'}), 403 

def upload_to_db(mac, level, time=''):
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
        new_data = BleData(mac, level, time)
        response = create(new_data=new_data)

        return bleDataSchemaOne.jsonify(new_data)
    else:
        return -1


# delete all data from db
@bledata.route('/delete', methods=['DELETE'])
@token_required
def delete_all_data(current_user):
    num_rows_deleted = delete(bledata=True)
    if num_rows_deleted:
        return jsonify({'deleted':num_rows_deleted, 'error': None})
    else:
        return jsonify({'error':'Nothing deleted'}), 401