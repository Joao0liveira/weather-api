===================================================================================================================================================

# Weather App -> Python, FastAPI and MongoDB Cloud

===================================================================================================================================================

This app consists of a FastAPI server that handles to types of requests endpoints: 
-POST?id=<str> 
-GET?id=<str>

These endpoints trigger auxiliary services responsible to get data from the Open Weather API and store it into MongoDB collections

## FastAPI 
Chosen for this task due to its high performance, being based on OpenAPI standard, and automatic interactive documentation generation

## MongoDB Cloud
Used by its performance and easy to use integration




===================================================================================================================================================
Auxiliary Services
===================================================================================================================================================

# DB Manager:

Service responsible to handle the connection and interactions with MongoDB

# Weather Service:

Composed of two classes, WeatherManager and WeatherService.
Which have the objective of creating asynchronous parallel services based on multiple threads.
These services will retrieve data from the Open Weather API within the constraints of 60 calls/minute
These services will retrieve data from the Open Weather API 
within the constraints of 60 api_calls/minute, then store it into MongoDB cluster collection of a given ID.
When the limit of 60 is broken, the services have to 
wait the cooldown time, which is given by the difference of the time of the first call and the last one.


===================================================================================================================================================
# How to use
===================================================================================================================================================
- Clone the repositorie
- Build the docker image 
    Example: docker build . -t weather-api
- Run the image in the container binding the port that want to be used
    Example: docker run -ti -p 8000:8000 weather-api

-/api/v1/post endpoint -> Create a colletion into MongoDB with the id provided and start a Weather Data Gathering process
method allowed: post
parameter: id:str
Example: localhost:8000/api/v1/post?id=<id>

-/api/v1/get endpoint -> Retrieve the id, status of the data gathering process and the data stored 
method allowed: get
parameter: id:str
Example: localhost:8000/api/v1/get?id=<id>

## FastAPI Docs
You may access the GUI of FastAPI through localhost:8000/docs where you will be able to test the endpoints and their response

===================================================================================================================================================
# How to test
===================================================================================================================================================
Set the env variable API_TEST=1
Then on the /src 
run the command: pytest test.py
After the tests run the dbpurge.py file to clean the DB from test data






===================================================================================================================================================