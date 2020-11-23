from app import app, db
from app.models import BleData, User
from app.schemes import BleDataSchema
from flask import request, jsonify, abort, make_response
from sqlalchemy import func
import uuid # for public id 
from werkzeug.security import generate_password_hash, check_password_hash 
import jwt #for PyJWT authentication 
from datetime import datetime, timedelta 
from functools import wraps 


bleDataSchemaAll = BleDataSchema(many=True)
bleDataSchemaOne = BleDataSchema()

blacklist = set()


# documentation
@app.route('/')
def doc():
    return jsonify({'/hello':{'type':'GET', 'describe':'check token', 'token_req':True, 'response': {'remaining':'remaining time in minutes', 'valid': 'valid token or not', 'error':'error description'}},
                    '/singup':{'type':'POST','describe':'singup new user', 'token_req':False},
                    '/user/login':{'type':'POST','describe':'login', 'token_req':True, 'response':'token'},
                    '/user/logout':{'type':'DELETE','describe':'logout','token_req':True},
                    '/user/':{'type':'GET','describe':'list of users','token_req':True},
                    '/api/bledata/':{'type':'GET','describe':'all data from ble scanner','token_req':True},
                    '/api/bledata/?count=&page=':{'type':'GET','describe':'data with pagination','token_req':True},
                    '/api/bledata/upload':{'type':'POST','describe':'upload data to db','token_req':False},
                    '/api/bledata/delete':{'type':'GET','describe':'delete all data','token_req':True}})


# decorator for verifying the JWT 
def token_required(f): 
    @wraps(f) 
    def decorated(*args, **kwargs): 
        token = None
        # jwt is passed in the request header 
        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token']  
        if not token: 
            return jsonify({'error':'Login required', 'valid':False, 'remaining': None}), 401
        try: 
            # decoding the payload to fetch the stored details 
            if token in blacklist:
                raise Exception
            data = jwt.decode(token, app.config['SECRET_KEY']) 
            current_user = User.query.filter_by(public_id = data['public_id']).first() 
        except: 
            return jsonify({'error':'Invalid token', 'valid':False, 'remaining': None}), 401
        # returns the current logged in users contex to the routes 
        return  f(current_user, *args, **kwargs) 

    return decorated 


# check token
@app.route('/hello')
@token_required
def check_token(current_user):
    token = request.headers['x-access-token']
    data = jwt.decode(token, app.config['SECRET_KEY']) 
    return jsonify({'valid':True, 'remaining':int((data['exp']-datetime.now().timestamp())/60)})


# page not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found page', 'description':str(error)}), 404)