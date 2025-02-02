from fastapi import FastAPI
from pydantic import BaseModel

class product(BaseModel):
    name : str
    price : int


app = FastAPI()


@app.get("/")
def get_the_product():
    return {
        "message":"hello i am calling from get method"
    }

@app.post("/product",status_code=201)
def creat_product_item(product_data:product):
    return{
            "name" : product_data.name,
            "price": product_data.price
    }