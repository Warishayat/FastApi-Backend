from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


sql_data_base_url = "sqlite:///./testdb.db"
engine  = create_engine(sql_data_base_url,connect_args={"check_same_thread":False})
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)
base = declarative_base()