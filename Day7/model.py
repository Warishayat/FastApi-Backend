from sqlalchemy import Column,String,Integer,func,Boolean,DateTime
from database import base,engine
from datetime import datetime , timedelta

class CreatUser(base):

    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)  # Ensure this line exists
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


base.metadata.create_all(bind=engine)
