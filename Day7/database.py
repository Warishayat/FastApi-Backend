from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


database_url = "sqlite:///./test.db"

engine = create_engine(database_url)
LocalSession = sessionmaker(autocommit=False,autoflush=False,bind=engine)

base = declarative_base()