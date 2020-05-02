from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity, 
    fresh_jwt_required
    )
from models.command import CommandModel


class Command(Resource):
    
    @jwt_required
    def get(self, title): # this method fetches command using name from db
        # check if command exist with name and return a result in json
        Command = CommandModel.find_by_title(title)
        if Command:
            return Command.json()
        return {'message': "Command not found"}, 404
      

    @jwt_required
    def post(self, title):  # this method defines creating new command by post
        # this ensures the right objects are sent from request json
        parser = reqparse.RequestParser() 
        # defines the values to recieve from request json
        parser.add_argument('command',
        type=str,
        required=True,
        help='command cannot be left blank'

        )
        parser.add_argument('describtion',
        type=str,
        required=True,
        help='describtion cannot be left blank'

        )
        parser.add_argument('collection_id',
        type=int,
        required=True,
        help='collection id cannot be left blank'

        )
        # check if name already exist by calling class method find by name
        if CommandModel.find_by_title(title): 
            return {'message': "A command with title '{}' already exists".format(title)}, 400

        data = parser.parse_args()
        # get userid from jwt
        user_id = get_jwt_identity()
        command = CommandModel(title, data['command'], data['describtion'], data['collection_id'], user_id) 

        try:
            command.save_to_db() 
        except:
            return {"message": "An error occurred inserting command"}, 500

        return command.justjson(), 201

    @jwt_required
    def delete(self, title):
        claims = get_jwt_claims() # this allows us to access jwt claims defined in app.py
        if not claims['is_admin']: # checks if the claim value = is_admin as defines in app.py
            return {'message': 'Admin privilages needed'}

        command = CommandModel.find_by_name(title)
        if command: 
            try:
                command.delete_command()
            except:
                return {"message": "An error occurred deleting command"}, 500
        else:
            return {'message': 'command doesnt exist'}

        return {'message': 'command deleted'}

    @jwt_required
    def put(self, title): # this defines updating existing commands
        parser = reqparse.RequestParser() 
        # defines the values to recieve from request json
        parser.add_argument('command',
        type=str,
        required=True,
        help='command cannot be left blank'

        )
        parser.add_argument('describtion',
        type=str,
        required=True,
        help='describtion cannot be left blank'

        )
        data = parser.parse_args() 
        user_id = get_jwt_identity()
        # check if command exist, if None create it else update it
        command = CommandModel.find_by_title(title)
        
        if command is None: 
            command = CommandModel(title, data['command'], data['describtion'], data['collection_id'], user_id) 
        elif command.user_id == user_id: # it means command exists then update 
            command.title = title
            command.command = data['command']
            command.describtion = data['describtion']

        elif command.user_id != user_id: # if user not owner then cant edit
            return {'message': 'you cant edit'}, 400

        command.save_to_db() 
        
        return {
            'message': 'Command Updated',
            'data':[command.justjson()]
        }



class CommandList(Resource): # resource in python must be seperated by two new lines
    @jwt_optional # allows user to login optionally but we can return result based on login or not
    def get(self):
        user_id = get_jwt_identity() # this allows us to get user id from access token
        commands = [x.justjson() for x in CommandModel.query.all()] # this loops through all items as defined self in item model then return in json as defined in json method in item model
        if user_id: # if user id present in get_jwt_identity
            return commands, 200
        
        return {
            'commands': [x['title'] for x in commands],
            'message': 'more data available if you login in'
         }    


