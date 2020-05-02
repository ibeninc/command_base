from models.store import StoreModel

class Storefunctions():

    def __init__(self, name):
        self.name = name

    def store_id(self, name):
        store = StoreModel.get_store_id(name)
        if store:
            return store
            
        return {'message': 'Unable to get store id'}