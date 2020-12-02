from . import users
from app import app
from app.models import User
from app.db_operation import create, read, delete, update
from flask import request, jsonify, abort, make_response
import uuid # for public id 
from werkzeug.security import generate_password_hash, check_password_hash 
import jwt #for PyJWT authentication 
from datetime import datetime, timedelta 
from functools import wraps 
from app.views import token_required, blacklist


# get info about users
@users.route('/', methods =['GET']) 
@token_required
def get_users(current_user): 
    try:
        id = request.args['id']
    except:
        id = ''
    if not id:
        users = read(user=True) 
        output = [] 
        for user in users: 
            output.append({ 
                'public_id': user.public_id, 
                'email' : user.email, 
                'username': user.username,
                'id': user.id
            }) 
        return jsonify({'users': output, 'error':None}) 
    else:
        user = read(user=True, id=id)
        if user:
            return jsonify({'public_id': user.public_id, 
                            'email': user.email, 
                            'username': user.username, 
                            'id':user.id ,
                            'error':None})
        else:
            return jsonify({'error': 'Wrong id'}), 403


# loging user in, return token if susses
@users.route('/login', methods =['POST']) 
def login(): 
    # creates dictionary of form data
    try:
        auth = request.form
    except:
        auth = request.get_json()

    if not auth or not auth.get('email') or not auth.get('password'): 
        return jsonify({'error':'Missing email or password', 'response': None}), 401 
    
    user = read(email=auth.get('email'), user=True) 

    if not user: 
        return jsonify({'error':'User does not exist', 'response': None}), 401  

    if check_password_hash(user.password, auth.get('password')): 
        # generates the JWT Token 
        token = jwt.encode({'public_id':user.public_id, 
                            'exp':datetime.utcnow()+timedelta(minutes = 360)}, 
                            app.config['SECRET_KEY']) 

        return make_response(jsonify({'response':{'token':token.decode('UTF-8'), 
                                                'username':user.username, 
                                                'email':user.email, 
                                                'id':user.id}, 
                                    'error': None}), 201) 
    return jsonify({'error':'Wrong password', 'response': None}), 403 


# log user out
@users.route('/logout', methods=['DELETE'])
@token_required
def logout(current_user):
    token = None
    # jwt is passed in the request header 
    if 'x-access-token' in request.headers: 
        token = request.headers['x-access-token']  
    blacklist.add(token)
    return jsonify({'response': 'Successfully logged out', 'error': None}), 200


# registration new user  
@users.route('/signup', methods =['POST']) 
def signup(): 
    try:
        data = request.form
    except:
        data = request.get_json()
    username, email, password = data.get('username'), data.get('email'), data.get('password') 

    # checking for existing user 
    user = read(email=data.get('email'), user=True)
    if username and email and password:
        if not user: 
            # database ORM object 
            user = User( 
                public_id = str(uuid.uuid4()), 
                username = username, 
                email = email, 
                password = generate_password_hash(password) 
            ) 
            # insert user 
            create(new_user=user)
    
            return jsonify({'response':'Successfully registered','error': None}), 201  
        else: 
            return jsonify({'error':'User already exists. Please Log in', 'response': None}), 202  
    else:
        return jsonify({'error':'Missing username or email or password', 'response': None}), 403 


# update user data
@users.route('/update', methods=['PUT'])
@token_required
def update_data_of_user(current_user):
    try:
        data = request.form
    except:
        data = request.get_json()
    for key in data.keys():
        for value in data.getlist(key):
            if(key=='password'):
                value = generate_password_hash(value)
            if update(field=key, new_value=value, current_user=current_user):
                return jsonify({'response':'Succesfully updated', 'error':None})
            else:
                return jsonify({'error':'Something went wrong', 'response':None}), 403
    return jsonify({'error': 'Not data for update', 'response': None}), 401


# delete user with id
@users.route('/delete', methods=['DELETE'])
@token_required
def delete_user(current_user):
    try:
        user_id = int(request.args['id'])
    except:
        user_id = -1
    if user_id >= 0:
        if delete(id_user=user_id):
            if current_user.id == user_id:
                logout()
            return jsonify({'response':'Succesfully deleted user', 'error':None})
        else: 
            return jsonify({'error':'Something went wrong', 'response':None}), 403
    else:
        return jsonify({'error': 'Wrong user id', 'response':None}), 401