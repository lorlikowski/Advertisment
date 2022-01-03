from sqlalchemy import Integer, String, Column, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.sqlite import UU
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
    category = Column(Integer, ForeignKey("categories.id"))

    content = Column(Text) #TODO: specify content type
    #published

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("categories.id"))

    parent = relationship("Category", back_populates="subcategories", remote_side=[id])

    subcategories = relationship("Category", back_populates="parent")
