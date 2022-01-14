from sqlalchemy import  Column,  Integer, String, UniqueConstraint

from .database import Base




class Relation(Base):

    __tablename__ = "relations"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    object_id = Column(Integer, index=True)
    type = Column(String, index=True)
    
    UniqueConstraint('user_id', 'object_id', 'type', name='relation')

