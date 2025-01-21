from fastapi import FastAPI,Depends
from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship,Session
from typing import List
from fastapi import HTTPException  
from pydantic import BaseModel #for schemas 



app = FastAPI()


#define the database setup
data_base_url = "sqlite:///./test.db"
engine = create_engine(data_base_url,connect_args={"check_same_thread" : False})
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=(engine))

base = declarative_base()


#define the usere table
class User(base):
    __tablename__ = "student"
    #define columns
    id =Column(Integer,primary_key=True,index=True)
    name = Column(String,unique=True,index=True)
    degree = Column(String,unique=True,index=True)

base.metadata.create_all(bind=engine)


#dependency to get the database session

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



#Now will make the schemas
# schema 1 create the user

class CreatUser(BaseModel): 
    id:int
    name:str
    degree:str

class Userresponse(BaseModel):
    id:int
    name:str
    degree:str

    class config:
        orm_mode = True

#now i will go with my first endpoint
@app.post("/save-data/{id}")
def saveUser(user:CreatUser,db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id == user.id).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with this ID already exists"
        )
    new_user = User(
        id=user.id,
        name=user.name,
        degree=user.degree
    )
    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)   # Refresh the instance to get the updated state from the DB
    return new_user


#to retrive the data from the database
@app.get("/user-record/{id}",response_model=Userresponse)
def user_record(id:int,db:Session=Depends(get_db)):
    user_search = db.query(User).filter(User.id==id).first()
    if user_search:
        return user_search
    raise HTTPException(status_code=400,detail="user not found")


#endpoint-to-get-all-records
@app.get("/allrecords",response_model=List[Userresponse])
def RecordsAll(db:Session=Depends(get_db)):
    user_record = db.query(User).all()
    if not user_record:
        return HTTPException(status_code=400,detail="No record found in the tables")
        
    return user_record

#delet endpoint by some specific id
@app.delete("/delet-user-record/{id}",response_model=Userresponse)
def DeletUserRecord(id:int,db:Session=Depends(get_db)):
    data_user= db.query(User).filter(User.id == id).first()
    if not data_user:
        raise HTTPException(status_code=400,detail="Does not found any user with this id")
    db.delete(data_user)
    db.commit()
    return data_user

#update the specific user
@app.put("/update-user-record/{id}",response_model=Userresponse)
def UpdatedUserinformation(id:int,user:CreatUser,db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="error not found")
    db_user.name = user.name
    db_user.degree =user.degree
    #commit the update records
    db.commit()
    db.refresh(db_user)
    return db_user 