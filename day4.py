from fastapi import FastAPI,File,Form,Query,UploadFile,HTTPException
from enum import Enum
from pydantic import BaseModel
from typing import Union

#error handling in the fastapi

app = FastAPI()


@app.get("/")
def root(name:str,rolllnum:int):
    return{"name":name,"value":rolllnum}


@app.get("/home")
def home(name:str,rollnum:Union[str,None]=None):
    return{"name":name,"rollnum":rollnum}

#choose field
class choose_student(str,Enum):
    one = "alice"
    two = "Bob"
    three ="zack"

@app.get("/choose_name")
def choosstudent(model:choose_student):
    if model == "one":
        return {"messsage":"choose Alice"}
    elif model == "two":
        return {"messaeg":"achoose bob"}
    else:
        return{"message":"choose zack"}

#message request body
@app.post("/request")
def request(file:bytes=File()):
    return len(file)

#add the student name,age,and email to the datbase
class Addstudent(BaseModel):
    name:str
    age:int
    emai:str

@app.post("/passStudent")
def passStudent(form:Addstudent):
    return form

#upload File
@app.post("/fileUpload")
def FileUpload(file:UploadFile=File(),name:str=Form()):
    return {"name of file is":file.filename,"name of the student is":name}

#handling errors
#import httpExeception
@app.get("/Error")
def Errorhandling(roll:str): #error aahandling in fastapi
    if roll == "21368":
        return HTTPException(status_code=400,detail="you are not allowed in college to do some operation")
    else:
        return{
            "message":"you are good to go with this rollnumber"
        }
    

item_id= ["132","134","125","1455"] #error handlings in the fastapi
@app.get("/item/{item_id}")
def item(item:str=item_id):
    if item not in item_id:
        return HTTPException(status_code=400,detail="item not found")

