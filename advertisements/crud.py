from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from pydantic.error_wrappers import ErrorWrapper
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from . import models, schemas

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def get_advertisements_for_user(db: Session, user: str) -> List[models.Advertisement]:
    return db.query(models.Advertisement).filter(models.Advertisement.owner == user).all()

def get_visible_advertisements_for_user(db: Session, user: str) -> List[models.Advertisement]:
    date = datetime.now()
    return db.query(models.Advertisement).filter(models.Advertisement.owner == user, models.Advertisement.date_start <= date).all()


def get_advertisement_by_id(db: Session, advertisement_id: int, only_visible : bool = True):
    query = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id)
    if only_visible:
        date = datetime.now()
        query = query.filter(models.Advertisement.date_start <= date)
    return query.first()

def create_advertisement(db: Session, advertisement: schemas.AdvertisementCreate, user: str):
    date = datetime.now()
    extra_fields = {
        'date_created': date,
        'date_modified': date,
        'owner': user
    }
    if advertisement.category is not None:
        category = get_category_by_name(db, advertisement.category)
        if category is None:
            raise RequestValidationError([ErrorWrapper(ValueError("Invalid category"), loc="category")])
        extra_fields['category_id'] = category.id
    db_advertisement = models.Advertisement(**advertisement.dict(exclude={"category"}), **extra_fields)
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    
    return db_advertisement

def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    extra_fields = {}
    if category.parent is not None:
        parent = get_category_by_name(db, category.parent)
        if parent is None:
            raise RequestValidationError([ErrorWrapper(ValueError("Invalid parent category"), loc="parent")])
        extra_fields['parent_id'] = parent.id

    db_category = models.Category(**category.dict(exclude={'parent'}), **extra_fields)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

def serialize_advertisement(advertisement: models.Advertisement) -> schemas.AdvertisementModel:
    if advertisement.category is not None:
        advertisement.__dict__['category'] = advertisement.category.name
    return schemas.AdvertisementModel.from_orm(advertisement)

def serialize_category(category: models.Category) -> schemas.CategoryModel:
    if category.parent is not None:
        category.__dict__['parent'] = category.parent.name
    return schemas.CategoryModel.from_orm(category)