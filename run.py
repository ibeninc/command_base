from app import app
from db import db

db.init_app(app)

#this tells flask to run onload and the defined method create all tables defined in all models in the app
@app.before_first_request
def create_tables():
    db.create_all()