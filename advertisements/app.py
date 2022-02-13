from datetime import datetime
from typing import List, Optional
from urllib import request
from pydantic import BaseSettings
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

models.Base.metadata.create_all(bind=engine)

NOTIFICATIONS_SERVICE_HOST_URL=os.environ.get("NOTIFICATIONS_SERVICE_HOST_URL")


app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthJWTSettings(BaseSettings):
    authjwt_algorithm: str = "RS512"
    authjwt_public_key: str = open("RS512.key.pub", "r").read()
    # authjwt_private_key: str = open("RS512.key", "r").read()


@AuthJWT.load_config
def get_config():
    return AuthJWTSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# @app.get('/users/me/advertisements/', response_model=List[schemas.AdvertisementModel])
# def users_advertisements(user_id: str, db: Session = Depends(get_db)):
#     return crud.get_advertisements_for_user(db, user_id)


@app.post("/users/me/advertisements/", response_model=schemas.AdvertisementModel)
def create_advertisement(
    # user_id: str,
    advertisement: schemas.AdvertisementCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    user_id = str(Authorize.get_jwt_subject())
    # if current_user != user_id:
    # raise HTTPException(status_code=400, detail="No permission to create advertisement") #TODO: check exception type

    advertisement = crud.create_advertisement(db, advertisement, user=user_id)
    response = requests.post(NOTIFICATIONS_SERVICE_HOST_URL + 'advertisement', json={
        "advertisement_id": int(advertisement.id),
        "owner_id": int(user_id),
        "type": "create"
    })
    print(response.json())
    return crud.serialize_advertisement(advertisement)


@app.get("/users/me/advertisements/", response_model=List[schemas.AdvertisementModel])
def my_advertisements(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = str(Authorize.get_jwt_subject())

    advertisements = crud.get_advertisements_for_user(db, user_id)
    return [
        crud.serialize_advertisement(advertisement) for advertisement in advertisements
    ]


@app.get(
    "/users/{user_id}/advertisements/", response_model=List[schemas.AdvertisementModel]
)
def users_advertisements(
    user_id: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    Authorize.jwt_optional()
    # current_user = Authorize.get_jwt_subject()
    # if current_user is None or current_user != user_id:
    advertisements = crud.get_visible_advertisements_for_user(db, user_id)
    # else:
    # advertisements = crud.get_advertisements_for_user(db, user_id)

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
        extra_filters["date_start__lt"] = datetime.fromisoformat(date_start__lt)
    if date_start__gt is not None:
        extra_filters["date_start__gt"] = datetime.fromisoformat(date_start__gt)
    if date_end__lt is not None:
        extra_filters["date_end__lt"] = datetime.fromisoformat(date_end__lt)
    if date_end__gt is not None:
        extra_filters["date_end__gt"] = datetime.fromisoformat(date_end__gt)

    return [
        crud.serialize_advertisement(advertisement)
        for advertisement in crud.get_advertisements(
            db, limit=limit, offset=skip, ordering=ordering, **extra_filters
        )
    ]

@app.get(
    "/advertisements/popular/",
    response_model=List[schemas.AdvertisementModel],
)
def popular_advertisements(
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
    db: Session = Depends(get_db),
):

    return [
        crud.serialize_advertisement(advertisement)
        for advertisement in crud.get_popular_advertisements(
            db, limit, skip
        )
    ]


@app.get(
    "/advertisements/{advertisement_id}/", response_model=schemas.AdvertisementModel
)
def get_advertisement(
    advertisement_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    Authorize.jwt_optional()
    current_user = str(Authorize.get_jwt_subject())

    advertisement = crud.get_advertisement_by_id(
        db, advertisement_id, only_visible=current_user is None
    )

    if advertisement is None or (
        not advertisement.visible and advertisement.owner != current_user
    ):
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return crud.serialize_advertisement(advertisement)


@app.get(
    "/advertisements/{advertisement_id}/content",
    response_model=schemas.AdvertisementContent,
)
def get_advertisement_content(
    advertisement_id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    Authorize.jwt_optional()
    current_user = str(Authorize.get_jwt_subject())

    advertisement = crud.get_advertisement_by_id(
        db, advertisement_id, only_visible=current_user is None
    )

    if advertisement is None or (
        (not advertisement.visible) and advertisement.owner != current_user
    ):
        raise HTTPException(status_code=404, detail="Advertisement not found")

    return advertisement


@app.put(
    "/advertisements/{advertisement_id}/", response_model=schemas.AdvertisementModel
)
def update_advertisement(
    advertisement_id: int,
    advertisement_update: schemas.AdvertisementUpdate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    current_user = str(Authorize.get_jwt_subject())

    advertisement = crud.get_advertisement_by_id(
        db, advertisement_id, only_visible=False
    )

    if advertisement is None or advertisement.owner != current_user:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    advertisement = crud.update_advertisement(db, advertisement, advertisement_update)
    httpx.post(NOTIFICATIONS_SERVICE_HOST_URL + 'advertisement', data={
        "advertisement_id": int(advertisement.id),
        "owner_id": int(current_user),
        "type": "update"
    })
    return crud.serialize_advertisement(advertisement)


@app.post(
    "/advertisements/{advertisement_id}/update_views",
    response_model=schemas.AdvertisementViews,
)
def update_advertisement_views(advertisement_id: int, db: Session = Depends(get_db)):
    advertisement = crud.get_advertisement_by_id(db, advertisement_id)
    if advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")

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
def advertisements_in_category(
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
        for advertisement in crud.get_advertisements_in_category(
            db, category_obj, limit, skip
        )
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
