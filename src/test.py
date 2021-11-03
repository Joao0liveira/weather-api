from fastapi.testclient import TestClient
from fastapi import FastAPI
from pymongo import MongoClient
from src.routes.services.db_manager import DBManager
from src.routes.api import router
import time

app = FastAPI()
app.include_router(router)
client = TestClient(app)

base_url = 'http://127.0.0.1:8000/api/v1'

def test_route_post():
    id = 'test-alfa'
    response = client.post(base_url+f"/post?id={id}")
    assert response.status_code == 200
    assert response.json() == [f"Id Created - {id}"]

def test_route_post_duplicated_id():
    id = 'test-alfa'
    time.sleep(5)   
    response = client.post(base_url+f"/post?id={id}")
    assert response.status_code == 200
    assert response.json() == [f"Invalid ID - {id}"]

def test_route_get():
    id = 'test-alfa'
    response = client.get(base_url+f"/get?id={id}")
    assert response.status_code == 200
    
def test_route_get_not_found():
    id = 'test-non-null'
    response = client.get(base_url+f"/get?id={id}")
    assert response.status_code == 200
    assert response.json() == [f"Invalid ID : ID not found in the DB - {id}"]


    