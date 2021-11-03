"""
===================================================================================================================================================

Weather App

This app consists of a FastAPI server that handles to types of requests endpoints: 
-POST?id=<str> 
-GET?id=<str>

These endpoints trigger auxiliary services responsible to get data from the Open Weather API and store it into MongoDB collections

--------------------------------------------------------------------------------------------------------------------------------------------------
Auxiliary Services
--------------------------------------------------------------------------------------------------------------------------------------------------

-DB Manager:

Service responsible to handle the connection and interactions with MongoDB

-Weather Service:

Composed of two classes, WeatherManager and WeatherService.
Which have the objective of creating asynchronous parallel services based on multiple threads.
These services will retrieve data from the Open Weather API within the constraints of 60 calls/minute
These services will retrieve data from the Open Weather API 
within the constraints of 60 api_calls/minute, then store it into MongoDB cluster collection of a given ID.
When the limit of 60 is broken, the services have to 
wait the cooldown time, which is given by the difference of the time of the first call and the last one.


===================================================================================================================================================

"""

from fastapi import FastAPI
from routes.api import router

app = FastAPI()

app.include_router(router)

