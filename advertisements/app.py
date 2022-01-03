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

@app.post('/users/{user_id}/advertisements/', response_model=schemas.AdvertisementModel)
def create_advertisement(user_id: str, advertisement: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    return crud.create_advertisement(db, advertisement, user=user_id)


@app.get('/users/{user_id}/advertisements/', response_model=List[schemas.AdvertisementModel])
def users_advertisements(user_id: str, db: Session = Depends(get_db)):
    return crud.get_advertisements_for_user(db, user_id)

@app.get('/advertisements/{advertisement_id}/', response_model=schemas.AdvertisementModel)
def get_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)

    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return advertisement

@app.get('/advertisements/{advertisement_id}/content', response_model=schemas.AdvertisementContent)
def get_advertisement_content(advertisement_id: int, db: Session = Depends(get_db)):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)

    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return advertisement

@app.post('/categories/', response_model=schemas.CategoryModel)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@app.get('/categories/', response_model=List[schemas.CategoryModel])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)
