from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class AdvertisementBase(BaseModel):
    title: str
    description: str
    date_start: datetime
    date_end: datetime



class AdvertisementModel(AdvertisementBase):
    id: int
    category: Optional[str]
    views: int
    owner: int

    class Config:
        orm_mode = True

class AdvertisementCreate(AdvertisementBase):
    content: str
    category: Optional[str]

class AdvertisementViews(BaseModel):
    views: int

    class Config:
        orm_mode = True

class AdvertisementContent(BaseModel):
    content: str

    class Config:
        orm_mode = True

class AdvertisementUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    content: Optional[str]

class CategoryBase(BaseModel):
    name: str
    parent: Optional[str]

class CategoryCreate(CategoryBase):
    pass


class CategoryModel(CategoryBase):
    advertisements_count: int
    class Config:
        orm_mode = True