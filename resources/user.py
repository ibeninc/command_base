from flask_restful import Resource, reqparse
from models.user import UserModel
# library for comparing strings
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_refresh_token_required, 
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
    )
from blacklist import BLACKLIST

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="This field cannot be blank."
        )
    parser.add_argument('password',
    type=str,
    required=True,
    help="This field cannot be blank."
        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'User created successfully', 'data':[user.json()] }, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        user.delete_from_db()
        return {'message': 'user deleted'}

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="This field cannot be blank."
        )
    parser.add_argument('password',
    type=str,
    required=True,
    help="This field cannot be blank."
        )
    
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data['username']) # find user in the database by username
        if user and safe_str_cmp(user.password, data['password']): # if user exist then compare password in user with the passed password
            access_token = create_access_token(identity=user.id, fresh=True) # jwt extended will create an access token using the user id
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'invalid login credentials'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) # when access token is fresh it means the user loged in with username and password if not fresh means the token was refreshed
        return {access_token: new_token}, 200

class UserLogout(Resource): 
    @jwt_required 
    def post(self):
        jti = get_raw_jwt()['jti'] #jti refers to jwt ids
        BLACKLIST.add(jti)
        return {'message': 'Successfuly logged out'}