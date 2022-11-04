import json

from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import current_user

from users.models import User as UserModel
from utils.encoder import AlchemyEncoder
from utils.logs import create_logger


class User(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        help='Email is required')
    parser.add_argument('password', type=str, required=True,
                        help='Password is required')

    def post(self):
        data = UserModel.parser.parse_args()
        email = data['email']
        password = data['password']

        user = UserModel.query.filter_by(email=email).one_or_none()
        if not user or not user.check_password(password):
            return {'message': 'Wrong email or password.'}, 401
        # Notice that we are passing in the actual sqlalchemy user object here
        access_token = create_access_token(
            identity=json.dumps(user, cls=AlchemyEncoder))
        return jsonify(access_token=access_token)

    @jwt_required()  # Requires dat token
    def get(self):
        # We can now access our sqlalchemy User object via `current_user`.
        return jsonify(
            id=current_user.id,
            full_name=current_user.full_name,
            email=current_user.email,
        )


class UserRegister(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        help='Username is required.')
    parser.add_argument('password', type=str, required=True,
                        help='Password is required.')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {'message': 'User already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201
