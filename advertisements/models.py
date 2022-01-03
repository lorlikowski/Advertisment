from sqlalchemy import Integer, String, Column, DateTime, Text
from sqlalchemy.dialects.sqlite import UU
# from sqlalchemy.orm import relationship

from .database import Base

class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True) #TODO: postgresql UUID?
    title = Column(String, index=True)
    description = Column(String)#TODO: length
    date_created = Column(DateTime, index=True)
    date_modified = Column(DateTime, index=True)
    date_start = Column(DateTime, index=True)
    date_end = Column(DateTime, index=True)

    content = Column(Text) #TODO: specify content type
    #published

#TODO: categories or tags
