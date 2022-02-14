from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
import os

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQL_DATABASE_URL = os.getenv('DATABASE_URI')
SQL_DATABASE_URL_REPLICA = os.getenv('DATABASE_URI_REPLICA')

engines = {
    'master': create_engine(SQL_DATABASE_URL),
    'replica': create_engine(SQL_DATABASE_URL_REPLICA),
}

class RoutingSession(Session):
    
    def get_bind(self, mapper=None, clause=None):
        if self._flushing:
            return engines['master']
        else:
            return engines['replica']

SessionLocal = scoped_session(sessionmaker(class_=RoutingSession, autocommit=False, autoflush=False))

Base = declarative_base()