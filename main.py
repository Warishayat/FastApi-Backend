from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.declarative import declarative_base
import jwt

# Constants for JWT
SECRET_TOKEN = "makemeSecret"
ALGORITHAM = "HS256"

# FastAPI app initialization
app = FastAPI()

# OAuth2 password bearer for token handling
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Database connection settings
database_url = "sqlite:///./UserSetting.db"
engine = create_engine(database_url)
Localsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

# Password hashing context (for encryption)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash passwords
def get_password_hash(passw):
    return pwd_context.hash(passw)

# Function to verify the password
def verify_password(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)

# Database model (SQLAlchemy)
class userModels(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    is_Activate = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    registerd_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=False, default=None, onupdate=func.now())
    created_at = Column(DateTime, nullable=False, server_default=func.now())

# Create the database tables
base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = Localsession()
    try:
        yield db
    finally:
        db.close()

# Schemas (Pydantic models for validation)
class LoginSchema(BaseModel):
    name: str
    password: str

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_Activate: bool
    is_verified: bool
    registerd_at: datetime
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True

# JWT Token Generation
def get_token(user: userModels):
    expiration = datetime.utcnow() + timedelta(minutes=20)
    payload = {"id": user.id, "email": user.email}
    access_token = jwt.encode(payload, SECRET_TOKEN, algorithm=ALGORITHAM)
    return access_token

# Token verification and user retrieval
def get_user_from_token(db: Session, token: str = Depends(OAuth2_scheme)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=[ALGORITHAM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Retrieve the user from the database
        user = db.query(userModels).filter(userModels.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Function to check if the user is activated and verified
def verify_access(user: userModels):
    if not user.is_Activate:
        raise HTTPException(
            status_code=400,
            detail="Your account is inactive",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Your account is unverified, we have resent the verification email",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Create user API
@app.post("/create-user", response_model=UserResponse)
async def create_user_account(data: CreateUserRequest, db: Session = Depends(get_db)):
    db_user = db.query(userModels).filter(userModels.email == data.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    new_user = userModels(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=get_password_hash(data.password),
        is_Activate=False,
        is_verified=False,
        registerd_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse.from_orm(new_user)

# User login API
@app.post("/login", response_model=UserResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(userModels).filter(userModels.email == data.name).first()
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )
    if not verify_password(data.password, db_user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )
    token = get_token(db_user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
    }

# Get user profile (protected)
# @app.get("/profile", response_model=UserResponse)
# async def get_user_profile(db: Session = Depends(get_db), user: userModels = Depends(get_user_from_token)):
#     # Verify that the user is activated and verified
#     verify_access(user)
#     return user
