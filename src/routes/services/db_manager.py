"""
DBManager:
An auxiliary service responsible 
to handle the connection and interactions with MongoDB
"""
from warnings import catch_warnings
from pymongo import MongoClient
import os
import json
from datetime import date, datetime
import logging
# Error logging config
logging.basicConfig(filename='db.log', level=logging.DEBUG)

# Path to the file wiht MongoDB keys and paths to access it
api_config_file = os.path.join(os.getcwd(),'config','dbconfig.json') 
with open(api_config_file, 'r') as file:
    keys = json.load(file)

class DBManager():
    """
    Class responsible to handle connections and transactions with MongoDB
    """
    def __init__(self) -> None:
        self.connect()
        pass


    def connect(self):
        """ Create a connection instace with MongoDB """
        try:
            client = MongoClient(keys['path'])
            self.weather_db = client['weather-app']
        except Exception as e:
            print(e)
            logging.error(e)           


    def id_exist(self, id:str) -> bool:
        """ 
        Auxiliary function to be used to check 
        if a given ID already exists in the DB

        Check if the provided user already exist 
        
        Parameter:
        id: str
        """
        return id in self.weather_db.list_collection_names() 

    def add_id(self, id:str):
        """ 
        Create a collection in the DB over a given ID 

        Parameter:
        id: str
        """
        db = self.weather_db[id]
        pass
        

    def add_city_data(self, id, obj):
        """ 
        Create a weather data document over a given ID collection 

        Parameter:
        id: str
        obj: {
            id:str,
            timestamp:datetime,
            city_id:int,
            temp:float,
            humidity:float
        }
        """
        db = self.weather_db[id]
        obj['id'] = id
        obj['timestamp'] = datetime.now()
        db.insert_one(obj)
        

    def data_by_id(self, id:str):
        """
        Retrieve the status of the Weather Data Gathering 
        of a given ID that already exists in the DB

        Parameter:
        id: str

        Return:
        Json data containing the requested ID, the process status and the Weather Data collected

        """
        db = self.weather_db[id]
        data = []
        for doc in db.find({}):
            data.append({
                "id":doc['id'],
                "timestamp":str(doc['timestamp']),
                "city_id":doc['city_id'],
                "temp":doc['temp'],
                "humidity":doc['humidity'],

            })
        status = (len(data) / 167) * 100
    
        return json.dumps({"id": id,"status":f"{round(status, 2)} % Complete" ,"data":data})
        


    

