from fastapi import FastAPI,Query,File,UploadFile
from typing import Union
from enum import Enum

app = FastAPI()


@app.get("/") #get request to get the data from the database
def root():
    return {"message":"hello i am calling from welcome page"}

#pass parameter with the get request
@app.get("/fromdata")
def formdata(name:str,rollnum:int):
    return {"name":name,"rollnum":rollnum}

#pass the default value to the parameters
@app.get("/default_value_form")
def default_value(name:str,rollnum : Union[str,None]=None):
    return {"name" : name ,"rollnum":rollnum}

#pass some kind of variable if user is not inout the valid inout it automatially take that value
@app.get("/getValueDefault")
def defaultValue(name: Union[str,None]=None,rollnum:Union[str,None]=None):
    return {"name": name,"rollnum":rollnum}