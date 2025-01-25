from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


database_url = "sqlite:///./Test.db"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

base= declarative_base()