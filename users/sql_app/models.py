from sqlalchemy import  Column,  Integer, String, UniqueConstraint
from sqlalchemy.sql.sqltypes import Boolean, LargeBinary

from .database import Base




class User(Base):

    __tablename__ = "userss"


    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(LargeBinary)
    is_active = Column(Boolean, default=True)

