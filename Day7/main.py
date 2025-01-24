from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import LocalSession
from model import CreatUser
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jwt import PyJWTError, decode
from typing import List


# Dependency to get DB session
def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()

SECRET_KEY = "makemesecretfrom the world"
ALGORITHAM = "HS256"
#to get the token from token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

# Initialize the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password hashing and verification functions
def hash_password(plain_pass):
    return pwd_context.hash(plain_pass)

def verify_pass(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)

# JWT Token creation function
def creat_new_token(user):
    claim = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(claim, SECRET_KEY, ALGORITHAM)

#decode the token
def decode_the_token(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        # Decode the JWT token
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHAM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # Query the user from the database
        user = db.query(CreatUser).filter(CreatUser.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if the user is active
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User is inactive. Access denied.")

        return user  # Return the user object for use in the route
    except PyJWTError:
        raise HTTPException(status_code=401,detail="TokenError")
        



class TokenResponse(BaseModel):
    token: str
    type: str
    

# Pydantic schemas
class CreatUserRequest(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    name: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True

class LoginUser(BaseModel):
    email: str
    password: str



# Create a new user
@app.post("/create-user", response_model=UserResponse)
def create_user(data: CreatUserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(CreatUser).filter(CreatUser.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    new_user = CreatUser(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        is_active=data.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# Login endpoint
@app.post("/login", response_model=TokenResponse)
def login(data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    db_user = db.query(CreatUser).filter(CreatUser.name == data.username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Email is not registered")

    if not verify_pass(data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="Your account is deactivated. Please contact support.")

    token = creat_new_token(db_user)
    return {"token": token, 
            "type": "bearer",
            "email":db_user.email,
            "password":db_user.password}

# Endpoint to read users (all active users)
@app.get("/users/", response_model=List[LoginUser])
def read_users(db: Session = Depends(get_db)):
    # Fetch all active users from the database
    users = db.query(CreatUser).filter(CreatUser.is_active == True).all()

    if not users:
        raise HTTPException(status_code=404, detail="No active users found")

    return users


# Protected route that requires a valid token
@app.get("/protected-route/", response_model=LoginUser)
def protected_route(current_user: CreatUser = Depends(decode_the_token)):
    return {
        "message": f"Welcome, {current_user.name}!",
        "email": current_user.email
    }