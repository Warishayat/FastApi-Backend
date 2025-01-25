from database import engine,SessionLocal,base
from models import User_creat
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel

app = FastAPI()


class Creat(BaseModel):
    name:str
    email:str
    password:str


class ValidateUser(BaseModel):
    id:int
    name:str
    email:str
    password:str
    is_activate : bool
    is_verified : bool
    class Config:
        orm_mode= True

#get tyhe databse session
def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

#creatUser in the database
@app.post("/creat-user",response_model=Creat)
async def creat_user(data:Creat,db:Session=Depends(get_db)):
    user = db.query(User_creat).filter(User_creat.email == data.email).first()

    if user:
        raise HTTPException(
            status_code=404,
            detail ="THIS EMAIL IS ALREADY REGISTERD"
        )
    new_user = User_creat(
        name = data.name,
        email = data.email,
        password = data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user





