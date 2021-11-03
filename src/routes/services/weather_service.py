"""
=========================================================================================================================

-Weather Service

Composed of two classes, WeatherManager and WeatherService.

Which have the objective of creating asynchronous parallel services based on multiple threads.

These services will retrieve data from the Open Weather API within the constraints of 60 calls/minute

These services will retrieve data from the Open Weather API 

within the constraints of 60 api_calls/minute, then store it into MongoDB cluster collection of a given ID.

When the limit of 60 is broken, the services have to 

wait the cooldown time, which is given by the difference of the time of the first call and the last one.

=========================================================================================================================
"""

from threading import Thread
from queue import Queue
import time
import requests
import os
import json
from .db_manager import DBManager


import logging

logging.basicConfig(filename='weather service.log', level=logging.DEBUG)



# Define the max number od threads to be used
WORKERS = 5
API_TEST = int(os.getenv('API_TEST'))

class WeatherManager():
    """ 
    Static class responsible to manage and synchronize the open weather APIs calls
    
    """
    
    # Variable to be used to check if the weather API may be called
    _allowed = True
    
    # Variable to be used to store the time frame of the requests
    _first_request_time = None
    
    # Variable to be used to track the number of asynchronous weather API calls made by distinct threads
    calls_made = Queue()

    # Method used to retrieve the state of the private variable _allowed
    @classmethod
    def allowed(cls) -> bool:
        return cls._allowed
    # Method used to change the state of the _allowed variable and wait until 60 seconds pass to liberate future API calls
    @classmethod
    def block(cls) -> None:
        cls._allowed = False
        time.sleep(cls.count_time())
    # Method used to change the state of the _allowed variable, flush the number of call_mades, 
    # and set a new time for _first_time_resquest
    @classmethod
    def release(cls) -> None:
        cls._first_request_time = None
        cls.flush_count()
        cls.set_time()
        cls._allowed = True

    # Method used to set the value to the _first_time_request variable
    @classmethod
    def set_time(cls):
        if cls._first_request_time == None: 
            cls._first_request_time = time.time()

    # Method used to check the time elapsed from the first API call of this cycle
    @classmethod
    def count_time(cls):
        if cls._first_request_time != None : 
            return time.time() - cls._first_request_time  
    # Method used to flush the _first_time_request variable
    @classmethod
    def flush_time(cls):
        cls._first_request_time = None

    # Method used to increment the number of weather API calls
    @classmethod
    def increment_call(cls, id):
        cls.calls_made.put(id)
    
    # Method used to retrieve the number of API calls, stored in the calls_made queue
    @classmethod
    def calls_count(cls):
        return cls.calls_made.qsize()

    # Method used to flush calls_made queue
    @classmethod
    def flush_count(cls):
        with cls.calls_made.mutex:
            cls.calls_made.queue.clear()
    

class WeatherService():
    """
    Class responsible to instantiate parallel API calls based on multiple threads
    """

    def __init__(self, id:str, keys:dict) -> None:
        
        self.id = id
        self.url = keys['url']
        self.citie_ids = Queue()
        self.appid = keys['appid']
        self.db_manager = DBManager()
        if API_TEST == 1:
            [ self.citie_ids.put(city) for city in keys['ids'][:2] ]
        else:
            [ self.citie_ids.put(city) for city in keys['ids'] ]
               

    # Method used to call the Weather API and store its data into the DB
    def get_city_weather_data(self, city_id:int):
        payload = {
        'id':str(city_id), 
        'appid':self.appid}
        url = self.url

        r = requests.get(url, params=payload)
        # Increment the number of api calls made
        WeatherManager.increment_call(city_id)
        # Parse json data to dict
        data = json.loads(r.text)
        obj = {
        'city_id':data['id'],
        'temp':round((data['main']['temp'] - 273),2),
        'humidity':data['main']['humidity']
        }
        self.db_manager.add_city_data(self.id, obj)
        

    # Method used to loop through all queued city ids and call the Open Weather API
    def service_loop(self):
        while self.citie_ids.qsize() > 0:
            if WeatherManager.allowed():
                if WeatherManager.calls_count() < 60:
                    id = self.citie_ids.get()
                    self.get_city_weather_data(id)
                elif WeatherManager.calls_count() >= 60 and WeatherManager.count_time() < 60:
                    WeatherManager.block()
                    WeatherManager.release()
            else:
                time.sleep(5)
    # Method used to create multiple threads running the loop service
    def get_all_cities_weather_data(self):
        WeatherManager.set_time()
        for _ in range(WORKERS):
            t = Thread(target=self.service_loop)
            t.start()

