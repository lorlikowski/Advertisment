from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):

    email: str

    

class UserCreate(UserBase):

    password: str
    is_admin: bool

class UserChange(UserCreate):

    password1: str
    is_admin: Optional[bool]

class UserPublic(UserBase):
    is_admin: bool

    class Config:
        orm_mode = True

class UserLogin(UserBase):

    password: str



class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
