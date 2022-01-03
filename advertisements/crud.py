from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from . import models, schemas

def get_advertisements_for_user(db: Session, user: str) -> List[models.Advertisement]:
    return db.query(models.Advertisement).filter(models.Advertisement.owner == user).all()

def get_advertisement_by_id(db: Session, advertisement_id: int):
    return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()

def create_advertisement(db: Session, advertisement: schemas.AdvertisementCreate, user: str):
    date = datetime.now()
    db_advertisement = models.Advertisement(**advertisement.dict(), owner=user, date_created=date, date_modified=date)
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    
    return db_advertisement

def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category