from . import users
from app import db
from app.models import User
from flask import request, jsonify, abort, make_response
from sqlalchemy import func
import uuid # for public id 
from werkzeug.security import generate_password_hash, check_password_hash 
import jwt #for PyJWT authentication 
from datetime import datetime, timedelta 
from functools import wraps 
from app.views import token_required


# get list of users
@users.route('/', methods =['GET']) 
@token_required
def get_all_users(current_user): 
    users = User.query.all() 
    output = [] 
    for user in users: 
        output.append({ 
            'public_id': user.public_id, 
            'email' : user.email, 
            'username': user.username
        }) 
    return jsonify({'users': output}) 


# loging user in, return token if susses
@users.route('/login', methods =['POST','GET']) 
def login(): 
    if request.method == 'POST':
        # creates dictionary of form data 
        auth = request.get_json()
    
        if not auth or not auth.get('email') or not auth.get('password'): 
            return jsonify({'error':'Missing email or password', 'response': None}), 401 
    
        user = User.query.filter_by(email = auth.get('email')).first() 
    
        if not user: 
            return jsonify({'error':'User does not exist', 'response': None}), 401  
    
        if check_password_hash(user.password, auth.get('password')): 
            # generates the JWT Token 
            token = jwt.encode({'public_id':user.public_id, 'exp':datetime.utcnow()+timedelta(minutes = 360)}, app.config['SECRET_KEY']) 
    
            return make_response(jsonify({'token':token.decode('UTF-8'), 'username':user.username, 'email':user.email}), 201) 
        return jsonify({'error':'Wrong password', 'response': None}), 403 
    if request.method == 'GET':
        return jsonify({'error':'use POST request'})


# log user out
@users.route('/logout', methods=['DELETE'])
@token_required
def logout(current_user):
    token = None
    # jwt is passed in the request header 
    if 'x-access-token' in request.headers: 
        token = request.headers['x-access-token']  
    if not token: 
        return jsonify({'error':'Login required', 'response':None}), 401
    blacklist.add(token)
    return jsonify({'response': 'Successfully logged out', 'error': None}), 200


# registration new user  
@users.route('/signup', methods =['POST','GET']) 
def signup(): 
    if request.method == 'POST':
        data = request.get_json()
        username, email, password = data.get('username'), data.get('email'), data.get('password') 

        # checking for existing user 
        user = User.query.filter_by(email = data.get('email')).first() 
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
                db.session.add(user) 
                db.session.commit() 
        
                return jsonify({'response':'Successfully registered','error': None}), 201  
            else: 
                return jsonify({'error':'User already exists. Please Log in', 'response': None}), 202  
        else:
            return jsonify({'error':'Missing username or email or password', 'response': None}), 403 
    if request.method == 'GET':
        return jsonify({'error':'use POST request'})