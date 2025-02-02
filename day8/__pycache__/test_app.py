from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app

#pip install pytest

client = TestClient(app=app) #test client will take the app that is main application.

def test_return_correct_response():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK #respomse is ok
    assert response.json() == {"message":"hello i am calling from get method"}     #if response is ok it will return this


def test_creat_product_response():
    product_data = {"name" : "jacket","price": 12.0}
    response = client.post("/product",json=product_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == product_data
