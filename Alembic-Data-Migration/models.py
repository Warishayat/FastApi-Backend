from database import base
from database import engine
from sqlalchemy import Integer,String,Boolean,Column


class User_creat(base):

    __tablename__ = "user"

    id = Column(Integer,primary_key=True,index=False)
    name = Column(String(40))
    email = Column(String,unique=True,index=False)
    password= Column(String(25))
    is_activate = Column(Boolean, default=True)  
    is_verified = Column(Boolean, default=False) 


base.metadata.create_all(bind=engine)