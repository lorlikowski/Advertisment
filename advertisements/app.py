from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get('/users/me/advertisements/', response_model=List[schemas.AdvertisementModel])
# def users_advertisements(user_id: str, db: Session = Depends(get_db)):
#     return crud.get_advertisements_for_user(db, user_id)

@app.post('/users/{user_id}/advertisements/', response_model=schemas.AdvertisementModel)
def create_advertisement(user_id: str, advertisement: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    advertisement = crud.create_advertisement(db, advertisement, user=user_id)
    return crud.serialize_advertisement(advertisement)


@app.get('/users/{user_id}/advertisements/', response_model=List[schemas.AdvertisementModel])
def users_advertisements(user_id: str, db: Session = Depends(get_db)):
    advertisements = crud.get_visible_advertisements_for_user(db, user_id)
    return [crud.serialize_advertisement(advertisement) for advertisement in advertisements]

@app.get('/advertisements/{advertisement_id}/', response_model=schemas.AdvertisementModel)
def get_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)

    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return crud.serialize_advertisement(advertisement)

@app.get('/advertisements/{advertisement_id}/content', response_model=schemas.AdvertisementContent)
def get_advertisement_content(advertisement_id: int, db: Session = Depends(get_db)):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)

    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return advertisement

@app.post('/categories/', response_model=schemas.CategoryModel)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category_obj = crud.create_category(db, category)
    return crud.serialize_category(category_obj)

@app.get('/categories/', response_model=List[schemas.CategoryModel])
def get_categories(db: Session = Depends(get_db)):
    return [crud.serialize_category(category) for category in crud.get_categories(db)]


@app.get('/categories/{category}/subcategories/', response_model=List[schemas.CategoryModel])
def get_categories(category: str, db: Session = Depends(get_db)):
    category_obj = crud.get_category_by_name(db, category)
    if category_obj is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return [crud.serialize_category(subcategory) for subcategory in category_obj.subcategories]

@app.get('/categories/{category}/advertisements/', response_model=List[schemas.AdvertisementModel])
def advertisements_in_category(category: str, db: Session = Depends(get_db)):
    category_obj = crud.get_category_by_name(db, category)
    if category_obj is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return [crud.serialize_advertisement(advertisement) for advertisement in category_obj.advertisements]


#TODO: with recursive subcategories
