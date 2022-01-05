from sqlalchemy.orm import Session
from . import models, schemas

def get_following(db: Session, type: str, user_id: int):
    return db.query(models.Relation.object_id).filter(models.Relation.type == type, models.Relation.user_id == user_id).all()

def get_followers(db: Session, type:str, object_id: int):
    return db.query(models.Relation.user_id).filter(models.Relation.type == type, models.Relation.object_id == object_id).all()

def get_relation(db: Session, relation: schemas.RelationCreate):
    return db.query(models.Relation).filter_by(**relation.dict()).first()


def create_relation(db: Session, relation: schemas.RelationCreate):
    db_relation = models.Relation(**relation.dict())
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation
