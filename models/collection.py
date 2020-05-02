from flask import jsonify
from db import db

class CollectionModel(db.Model):
    __tablename__ = 'collections' # this tells sqlachemy our collection table
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    #this allows collection to know which command share its id with
    commands = db.relationship('CommandModel', lazy='dynamic') # lazy='dynamic' tell sqlalchemy that it should not fetch commands that share same id
   
    def __init__(self, name):
        self.name = name

    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name
        }

    def json(self): # this allows us to return a json representation of collectionmodel
        return {'id': self.id, 'name': self.name, 'Commands': [command.json() for command in self.commands.all()]} # this returns all the items related to the store

    # define a class method that will find command by name
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name limit to 1

    @classmethod
    def get_collection_id(cls, name):
        getid = cls.query.filter_by(name=name).first() 
        if getid:
            return jsonify({'data': [getid.serialized]})
    
    # define a method that will add collection into db
    def save_to_db(self):
        db.session.add(self) # self as defined above in the ItemModel is name, price
        db.session.commit()
    
    # define a method that will delete collection from db
    def delete_collection(self):
        db.session.delete(self)
        db.session.commit()
