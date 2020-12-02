from app import app
from flask import request, jsonify, make_response
from sqlalchemy import func
import jwt #for PyJWT authentication 
from datetime import datetime
from functools import wraps 
from app.db_operation import read


blacklist = set()


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
            current_user = read(public_id=data['public_id'], user=True)
        except: 
            return jsonify({'error':'Invalid token', 'valid':False, 'remaining': None}), 401
        # returns the current logged in users contex to the routes 
        return  f(current_user, *args, **kwargs) 
    return decorated 


# check token
@app.route('/hello', methods =['GET'])
@token_required
def check_token(current_user):
    token = request.headers['x-access-token']
    data = jwt.decode(token, app.config['SECRET_KEY']) 
    return jsonify({'valid':True, 'remaining':int((data['exp']-datetime.now().timestamp())/60)})


# documentation
@app.route('/')
def doc():
    return jsonify({'/hello':
                        {'type':'GET', 
                        'describe':'check token', 
                        'token_req':True, 'response': 
                            {'remaining':'remaining time in minutes', 
                            'valid': 'valid token or not', 
                            'error':'error description'}},
                    '/user/singup':
                        {'type':'POST',
                        'describe':'singup new user', 
                        'token_req':False},
                    '/user/login':
                        {'type':'POST',
                        'describe':'login', 
                        'token_req':True, 
                        'response': 'token, username, email, id'},
                    '/user/logout':
                        {'type':'DELETE',
                        'describe':'logout',
                        'token_req':True},
                    '/user/':
                        {'type':'GET',
                        'describe':'list of users',
                        'token_req':True},
                    '/user/delete?id=':
                        {'type':'DELETE',
                        'describe':'delete user with id',
                        'token_req':True},
                    '/user/?id=':
                        {'type':'GET'
                        ,'describe':'get user with id',
                        'token_req':True},
                    '/api/bledata/':
                        {'type':'GET',
                        'describe':'all data from ble scanner',
                        'token_req':True},
                    '/api/bledata/?count=&page=':
                        {'type':'GET',
                        'describe':'data with pagination',
                        'token_req':True},
                    '/api/bledata/ body: mac':
                        {'type':'GET',
                        'describe':'all data by mac',
                        'token_req':True}, 
                    '/api/bledata/upload':
                        {'type':'POST',
                        'describe':'upload data to db',
                        'token_req':False},
                    '/api/bledata/delete':
                        {'type':'GET',
                        'describe':'delete all data',
                        'token_req':True}})


# error handlers
@app.errorhandler(404)
def not_found(error):
    """
    Return a custom 404 Http response message for missing or not found routes.
    :param e: Exception
    :return: Http Response
    """
    return make_response(jsonify({'error':'not found page'}), 404)


@app.errorhandler(405)
def method_not_found(e):
    """
    Custom response for methods not allowed for the requested URLs
    :param e: Exception
    :return:
    """
    return make_response(jsonify({'error':'The method is not allowed for the requested URL'}), 405)


@app.errorhandler(500)
def internal_server_error(e):
    """
    Return a custom message for a 500 internal error
    :param e: Exception
    :return:
    """
    return make_response(jsonify({'error':'Internal server error'}), 500)