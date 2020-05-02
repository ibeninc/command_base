import os # this allows us to read system variables since we will be using heroku postgress 

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager 
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout # importing registeration resourse from user.py file
from resources.command import Command, CommandList
from resources.collection import Collection, CollectionList
from blacklist import BLACKLIST
#commandenv
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # this allows us to postgress from heroku on live server and sqlite on local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # allows us to see error raised by JWT in our app
app.config['JWT_BLACKLIST_ENABLED'] = True # this enables us to deny access for specific user ids
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] # this enable blacklist access to both jwt access and refresh token
app.secret_key = 'ruby'
api = Api(app)

jwt = JWTManager(app)


#this tells flask to create all tables defined in all models in the app when using local db
# @app.before_first_request
# def create_tables():
#     db.create_all()


#defining jwt claims
@jwt.user_claims_loader
def add_claims_to_jwt(identity): 
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

# this defines jwt blacklist list(wer are using this for logout to blacklist access token when logout)
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

# defining expired expired jwt
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'Login token has expired',
        'error': 'token_expired'
        }), 401

# this defines response for invalid token
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'invalid signature token',
        'error': 'token_invalid'
    }), 401

#this definess jwt unauthorized response
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'message': 'request does not contain an access token',
        'error': 'authorization required'
    }), 401

# this defines jwt needs fresh token
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'message': 'token is not fresh',
        'error': 'fresh_token_required'
    }), 401


#defines jwt response for revoking token
@jwt.revoked_token_loader
def revoke_token_callback():
    return jsonify({
        'message': 'token have been revoked',
        'error': 'token_invalid'
    }), 401



api.add_resource(Command, '/command/<string:title>')
api.add_resource(CommandList, '/commands')
api.add_resource(UserRegister, '/register') 
api.add_resource(Collection, '/collection/<string:name>')
api.add_resource(CollectionList, '/collections')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':  # this prevents app from running all its resourses should incase we import app.py in another file
    from db import db
    db.init_app(app)
    app.run(port=5000, debug='true')