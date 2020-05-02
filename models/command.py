from db import db


class CommandModel(db.Model):
    __tablename__ = 'commands' # this tells sqlachemy our user table
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    command = db.Column(db.String())
    describtion = db.Column(db.String())
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    collection = db.relationship('CollectionModel')
    user = db.relationship('UserModel')

    def __init__(self, title, command, describtion, collection_id, user_id):
        self.title = title
        self.command = command
        self.describtion = describtion
        self.collection_id = collection_id
        self.user_id = user_id

    def json(self): # this allows us to return a json representation of commandmodel 
        return {'id': self.id, 'title': self.title, 'command': self.command, 'describtion': self.describtion, 'collection_id': self.collection_id, 'user_id': self.user_id}


    def justjson(self):
        return {'title': self.title, 'command': self.command, 'describtion': self.describtion, 'collection_id': self.collection_id}

    # define a class method that will find a command by name
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first() # SELECT * FROM items WHERE title=title limit to 1
    
    # define a method that will add command into db
    def save_to_db(self):
        db.session.add(self) 
        db.session.commit()
    
    # define a method that will delete command from db
    def delete_command(self):
        db.session.delete(self)
        db.session.commit()
