from flask import Blueprint, jsonify, request

from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

from ..models import User

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/')
def index():
    return 'ok'

@auth_routes.route('/register', methods=['POST'])
def register():
    user = User.create(
        username=request.json['username'], 
        password_hash=User.get_password_hash(request.json['password'])
    )
    return jsonify({'username': user.username, 'id': user.id}), 201



@auth_routes.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(
        username=request.json['username']
    ).first()
    if user is None:
        return jsonify({'error': "incorrect username and password"}), 401
    if user.check_password(request.json['password']):
        return jsonify(
            {'username': user.username,
                'token': create_access_token(identity=user.id)}
        ), 200
    else:
        return jsonify({'error': "incorrect username and password"}), 401
