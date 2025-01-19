from fastapi import FastAPI,Query,Form
from enum import Enum
from typing import Union

app=FastAPI()
class choice_name(str,Enum):
    one="alice"
    two="Bob"
    Three="Martin"
@app.get("/home")
def Choice_Field(Model:choice_name):
    if Model == choice_name.one:
        return{
            "message" : Model
        }
    if Model == choice_name.two:
        return{
            "message" : Model,
        }
    else:
        return{
            "message"  : Model,
        }
    

#message request or post to sent the data to the database
from pydantic import BaseModel

class Schema1(BaseModel):
    name:str 
    classs:str
    rollnum: int

@app.post("/form")
def formdata(form:Schema1):
    return form
    
#fiel upload
from fastapi import File
@app.post("/fileUpload")
def fileupload(file:bytes=File()):
    return len(file)

#formdata
from fastapi import UploadFile,File,Form
@app.post("/Formm/")
def dataform(file:UploadFile=File(),name:str=Form()):
    return{
        "name of file is": file.filename,
        "name" : name
    }

@app.post("/form/data/")
def data(name:str=Form(),password:str=Form(),classs:str=Form()):
    return{
        "name" : name,
        "password" : password,
        "classs" : classs
    }