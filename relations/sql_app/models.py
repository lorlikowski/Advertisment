from sqlalchemy import  Column,  Integer, String, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()




class Relation(Base):

    __tablename__ = "relations"


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    object_id = Column(Integer, index=True)
    type = Column(String, index=True)
    
    UniqueConstraint('user_id', 'object_id', 'type', name='relation')

    __table_args__ = (
        Index("user_type", "user_id", "type"),
        Index("object_type", "object_id", "type"),
    )

