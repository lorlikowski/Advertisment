from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

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


@app.post("/users/{user_id}/advertisements/", response_model=schemas.AdvertisementModel)
def create_advertisement(
    user_id: str,
    advertisement: schemas.AdvertisementCreate,
    db: Session = Depends(get_db),
):
    advertisement = crud.create_advertisement(db, advertisement, user=user_id)
    return crud.serialize_advertisement(advertisement)


@app.get(
    "/users/{user_id}/advertisements/", response_model=List[schemas.AdvertisementModel]
)
def users_advertisements(user_id: str, db: Session = Depends(get_db)):
    advertisements = crud.get_visible_advertisements_for_user(db, user_id)
    return [
        crud.serialize_advertisement(advertisement) for advertisement in advertisements
    ]


@app.get("/advertisements/", response_model=List[schemas.AdvertisementModel])
def get_advertisements(
    title__contains: Optional[str] = None,
    date_start__lt: Optional[str] = None,
    date_start__gt: Optional[str] = None,
    date_end__lt: Optional[str] = None,
    date_end__gt: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
    ordering: Optional[crud.AdvertisementOrdering] = "views__dsc",
    db: Session = Depends(get_db),
):
    extra_filters = {}
    if title__contains is not None:
        extra_filters["title__contains"] = title__contains
    if date_start__lt is not None:
        extra_filters["date_start__lt"] = datetime.datetime(date_start__lt)
    if date_start__gt is not None:
        extra_filters["date_start__gt"] = datetime.datetime(date_start__gt)
    if date_end__lt is not None:
        extra_filters["date_end__lt"] = datetime.datetime(date_end__lt)
    if date_end__gt is not None:
        extra_filters["date_end__gt"] = datetime.datetime(date_end__gt)

    return [
        crud.serialize_advertisement(advertisement)
        for advertisement in crud.get_advertisements(
            db, limit=limit, offset=skip, ordering=ordering, **extra_filters
        )
    ]


@app.get(
    "/advertisements/{advertisement_id}/", response_model=schemas.AdvertisementModel
)
def get_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)

    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return crud.serialize_advertisement(advertisement)


@app.get(
    "/advertisements/{advertisement_id}/content",
    response_model=schemas.AdvertisementContent,
)
def get_advertisement_content(advertisement_id: int, db: Session = Depends(get_db)):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)

    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return advertisement


@app.put(
    "/advertisements/{advertisement_id}/", response_model=schemas.AdvertisementModel
)
def update_advertisement(
    advertisement_id: int,
    advertisement_update: schemas.AdvertisementUpdate,
    db: Session = Depends(get_db),
):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)
    advertisement = crud.update_advertisement(db, advertisement, advertisement_update)
    return crud.serialize_advertisement(advertisement)


@app.post(
    "/advertisements/{advertisement_id}/update_views",
    response_model=schemas.AdvertisementViews,
)
def update_advertisement_views(advertisement_id: int, db: Session = Depends(get_db)):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)
    return crud.increment_advertisement_view_count(db, advertisement)


@app.post("/categories/", response_model=schemas.CategoryModel)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category_obj = crud.create_category(db, category)
    return crud.serialize_category(category_obj)


@app.get("/categories/", response_model=List[schemas.CategoryModel])
def get_categories(db: Session = Depends(get_db)):
    return [crud.serialize_category(category) for category in crud.get_categories(db)]


@app.get(
    "/categories/{category}/subcategories/", response_model=List[schemas.CategoryModel]
)
def get_categories(category: str, db: Session = Depends(get_db)):
    category_obj = crud.get_category_by_name(db, category)
    if category_obj is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return [
        crud.serialize_category(subcategory)
        for subcategory in category_obj.subcategories
    ]


@app.get(
    "/categories/{category}/advertisements/",
    response_model=List[schemas.AdvertisementModel],
)
def advertisements_in_category(category: str, db: Session = Depends(get_db)):
    category_obj = crud.get_category_by_name(db, category)
    if category_obj is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return [
        crud.serialize_advertisement(advertisement)
        for advertisement in category_obj.advertisements
    ]


@app.get(
    "/categories/{category}/advertisements/popular/",
    response_model=List[schemas.AdvertisementModel],
)
def popular_advertisements_in_category(
    category: str,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
    db: Session = Depends(get_db),
):
    category_obj = crud.get_category_by_name(db, category)
    if category_obj is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return [
        crud.serialize_advertisement(advertisement)
        for advertisement in crud.get_popular_advertisements_in_category(
            db, category_obj, limit, skip
        )
    ]


# TODO: with recursive subcategories
