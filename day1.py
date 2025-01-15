from fastapi import FastAPI


app = FastAPI()

@app.get("/")  #endpoint
def read_root():
    return {"message": "Hello, World!"}

@app.get("/home/{name}") #endpoint2 and pass the paramters
def welcome_home(name:str):
    return {"welcome to the homepage":name}
 
@app.get("/add/{num1}/{num2}")
def addition(num1:int,num2:int):
    return {f"the addtion of {num1} + {num2} is =": num1+num2}

@app.get("/subtraction/{num1}/{num2}")
def subtraction(num1:int,num2:int):
    return {f"the subtraction on the number{num1} and {num2} is=":num1-num2}

@app.get("/divider/{num1}/{num2}")
def subtraction(num1:int,num2:int):
    return {f"the divider on the number{num1} and {num2} is=":num1/num2}

@app.get("/multiplication/{num1}/{num2}")
def subtraction(num1:int,num2:int):
    return {f"the multiplication on the number{num1} and {num2} is=":num1*num2}