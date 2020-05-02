from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.collection import CollectionModel


class Collection(Resource):
    def get(self, name):
        collection = CollectionModel.find_by_name(name)
        if collection:
            return collection.json()
            
        return {'message': 'collection not found'}, 404

    def post(self, name):
        #check if collection already exist
        if CollectionModel.find_by_name(name):
            return {'message': 'collection already exists'}
        
        collection = CollectionModel(name)
       
        try:
            collection.save_to_db()
            collection_id = CollectionModel.get_collection_id(name)
        except:
            return {'message': 'An error occurred while creating new collection'}, 500

        return collection_id

    
    def delete(self, name):
        #check if collection exist
        collection = CollectionModel.find_by_name(name)
        if collection:
            collection.delete_collection()

        return {'message': 'Collection deleted'}



class CollectionList(Resource):
    def get(self):
        return {'collections': [x.json() for x in CollectionModel.query.all()]}