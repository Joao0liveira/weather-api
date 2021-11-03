from fastapi import APIRouter
from .services.db_manager import DBManager
from .services.weather_service import WeatherService
import logging
import os
import json
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Path to the file wiht the weather api keys and paths
api_config_file = os.path.join(os.getcwd(),'config','service.json') 
with open(api_config_file, 'r') as file:
    keys = json.load(file)

# Router instance to be imported in the main app.py
router = APIRouter()
# Base url to be used in the endpoints
base_url = "/api/v1"


# Endpoint responsible to retrieve the Weather Data Gathering process
@router.get(base_url + "/get", 
tags=["data_request"],
summary="Get the status of given ID",
response_description="ID status"
)
async def get_by_id(id: str):
    """
    Get the status of the data gathering of a given ID
    \n
    \nParameters:
    \n- **id** : an Id the already exists on the DB
    
    \nErrors:
    \n- **Invalid ID** : ID not found in the DB


    """
    db = DBManager()
    if db.id_exist(id):
        return {db.data_by_id(id)}
    else:
        return {f"Invalid ID : ID not found in the DB - {id}"}
    
# Endpoint responsible to start the creation of the Weather Data Gatheing 
@router.post(base_url + "/post", 
tags=["data_request"],
summary='Create a Weather Data Gathering by the given ID',
response_description="Weather Data Request has started"

)
async def post_request(id: str):
    """
    Create a weather data gathering process 
    \n
    \nParameters:
    \n- **id** (string): Access key for the data gathering process
    
    \nErrors:
    \n- **Invalid ID** : ID already exists! Choose another one.


    """
    db = DBManager()
    if not db.id_exist(id):
        db.add_id(id)
        service = WeatherService(id, keys)
        service.get_all_cities_weather_data()
        return {f"Id Created - {id}"}

    else:
        return {f"Invalid ID - {id}"}

