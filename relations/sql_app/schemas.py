from pydantic import BaseModel

class RelationBase(BaseModel):

    user_id: int
    object_id: int
    type: str

    

class RelationCreate(RelationBase):
    pass



class Relation(RelationBase):
    id: int

    class Config:
        orm_mode = True
