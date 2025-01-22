from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import models  # This is where your `TransactionData` model is imported
from database import session, engine, base

app = FastAPI()

# Pydantic models for request validation
class TransactionBase(BaseModel):
    name: str
    amount: int
    discription: str

class TransactionModel(TransactionBase):
    id: int

    class Config:
        orm_mode = True

# Dependency to get the database session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# Create the tables (if they don't exist)
base.metadata.create_all(bind=engine)

# Create a new transaction (POST)
@app.post("/create-user", response_model=TransactionModel)
async def create_user(transaction: TransactionBase, db: Session = Depends(get_db)):
    db_transaction = models.TransactionData(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Fetch a transaction by ID (GET)
@app.get("/fetch-user/{id}", response_model=TransactionModel)
async def fetch_data(id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.TransactionData).filter(models.TransactionData.id == id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

# Fetch all transactions (GET)
@app.get("/fetch-all", response_model=List[TransactionModel])
async def fetch_all(db: Session = Depends(get_db)):
    db_transactions = db.query(models.TransactionData).all()
    if not db_transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return db_transactions
