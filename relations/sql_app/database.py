from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQL_DATABASE_URL = os.getenv('DATABASE_URI')
# SQL_DATABASE_URL2 = os.getenv('DATABASE_URI2')

# engines = [create_engine(SQL_DATABASE_URL), create_engine(SQL_DATABASE_URL2)]
engine = create_engine(SQL_DATABASE_URL)

# class RoutingSession(Session):
#     def get_bind(self, mapper=None, clause=None):
#         if mapper and issubclass(mapper.class_, Relation):
#             print("Engine", mapper.user_id % len(engines))
#             return engines[mapper.user_id % len(engines)]
#         else:
#             print("Default engine!")
#             return engines[0]


# SessionLocal = sessionmaker(autocommit=False, autoflush=False, class_=RoutingSession)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engines = [engine]