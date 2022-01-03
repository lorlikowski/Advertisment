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

    class Config:
        orm_mode = True

class AdvertisementCreate(AdvertisementBase):
    content: str
    # category: Optional[str] TODO: 


class AdvertisementContent(BaseModel):
    content: str

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass


class CategoryModel(CategoryBase):
    class Config:
        orm_mode = True