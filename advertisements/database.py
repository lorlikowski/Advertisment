from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQL_DATABASE_URL = os.getenv('DATABASE_URI')

engine = create_engine(
    SQL_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()