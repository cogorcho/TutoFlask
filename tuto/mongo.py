import pymongo
from pymongo import MongoClient
from flask import current_app, g
from flask.cli import with_appcontext

client = MongoClient('mongodb://localhost:27017')
#DB = client['Escuelas']
#collection = DB['Escuelas']

def get_db():
    if 'mongo' not in g:
        g.mongo = MongoClient('mongodb://localhost:27017')
        print(g.mongo)

    return g.mongo

def close_db(e=None):
    mongo = g.pop('mongo', None)

    if mongo is not None:
        mongo.close()
