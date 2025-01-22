from database import base 
from sqlalchemy import Column,Integer,String,Boolean



class TransactionData(base):
    __tablename__ = "Transaction"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    discription = Column(String)
    amount = Column(String)


