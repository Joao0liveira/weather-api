from pymongo import MongoClient
from src.routes.services.db_manager import DBManager
import sys
import os

"""

Utility used to clear the database

-a : delete all data in the DB
-t : delete test data in the DB


"""

def sanitize_db_test():
    db = DBManager()
    collections = db.weather_db.list_collection_names()
    names = [name for name in collections if 'test' in name]
    for name in names:
        collecion = db.weather_db[name]
        collecion.drop()

def sanitize_db():
    db = DBManager()
    collections = db.weather_db.list_collection_names()
    for name in collections:
        collecion = db.weather_db[name]
        collecion.drop()

if __name__=="__main__":
    env = os.getenv('API_TEST')
    if '-a' in sys.argv[-1]:
        sanitize_db()
    else:
        sanitize_db_test()
    