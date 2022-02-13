from enum import Enum
from datetime import datetime
from typing import Any, Dict, List, Union
from sqlalchemy.orm import Session
from pydantic.error_wrappers import ErrorWrapper
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
import models, schemas


def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()


def get_advertisements_for_user(db: Session, user: str) -> List[models.Advertisement]:
    return (
        db.query(models.Advertisement).filter(models.Advertisement.owner == user).all()
    )


def get_visible_advertisements_for_user(
    db: Session, user: str
) -> List[models.Advertisement]:
    date = datetime.now()
    return (
        db.query(models.Advertisement)
        .filter(
            models.Advertisement.owner == user, models.Advertisement.date_start <= date
        )
        .all()
    )


class AdvertisementOrdering(str, Enum):
    TITLE_ASC = "title"
    TITLE_DSC = "title__dsc"
    DATE_START_ASC = "date_start"
    DATE_START_DSC = "date_start__dsc"
    DATE_END_ASC = "date_end"
    DATE_END_DSC = "date_end__dsc"
    VIEWS_ASC = "views"
    VIEWS_DSC = "views__dsc"


advertisement_filter_columns = {
    "title": models.Advertisement.title,
    "date_start": models.Advertisement.date_start,
    "date_end": models.Advertisement.date_end,
    "views": models.Advertisement.views,
}


def get_advertisements(
    db: Session,
    limit: int,
    offset: int = 0,
    ordering: str = AdvertisementOrdering.VIEWS_DSC,
    **filters: Dict[str, any],
):
    processed_filters = []

    for field, value in filters.items():
        try:
            if field.endswith("__contains"):
                processed_filters.append(
                    advertisement_filter_columns[
                        field[: field.rfind("__contains")]
                    ].contains(value)
                )
            elif field.endswith("__gt"):
                processed_filters.append(
                    advertisement_filter_columns[field[: field.rfind("__gt")]] > value
                )
            elif field.endswith("__lt"):
                processed_filters.append(
                    advertisement_filter_columns[field[: field.rfind("__gt")]] < value
                )
        except KeyError:
            raise RequestValidationError(
                [
                    ErrorWrapper(
                        ValueError(f"Invalid query filter: ({field}, {value})"), field
                    )
                ]
            )

    if ordering not in list(AdvertisementOrdering):
        raise RequestValidationError(
            [
                ErrorWrapper(
                    ValueError(f"Invalid query ordering: {ordering}"), "ordering"
                )
            ]
        )
    if ordering.endswith("__dsc"):
        processed_ordering = advertisement_filter_columns[
            ordering[: ordering.rfind("__dsc")]
        ].desc()
    else:
        processed_ordering = advertisement_filter_columns[ordering]

    return (
        db.query(models.Advertisement)
        .filter(*processed_filters)
        .order_by(processed_ordering, models.Advertisement.id)
        .offset(offset)
        .limit(limit)
    )


def get_advertisement_by_id(
    db: Session, advertisement_id: int, only_visible: bool = True
):
    query = db.query(models.Advertisement).filter(
        models.Advertisement.id == advertisement_id
    )
    if only_visible:
        date = datetime.now()
        query = query.filter(models.Advertisement.date_start <= date)
    return query.first()


def create_advertisement(
    db: Session, advertisement: schemas.AdvertisementCreate, user: str
):
    date = datetime.now()
    extra_fields = {"date_created": date, "date_modified": date, "owner": user}
    if advertisement.category is not None:
        category = get_category_by_name(db, advertisement.category)
        if category is None:
            raise RequestValidationError(
                [ErrorWrapper(ValueError("Invalid category"), loc="category")]
            )
        extra_fields["category_id"] = category.id
    db_advertisement = models.Advertisement(
        **advertisement.dict(exclude={"category"}), **extra_fields
    )
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)

    return db_advertisement


def update_advertisement(
    db: Session,
    db_obj: models.Advertisement,
    update_data: Union[schemas.AdvertisementUpdate, Dict[str, Any]],
):
    if not isinstance(update_data, dict):
        update_data = update_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    print(update_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def increment_advertisement_view_count(
    db: Session, advertisement: models.Advertisement, incr: int = 1
):
    advertisement.views = models.Advertisement.views + incr
    db.commit()
    db.refresh(advertisement)
    return advertisement

def get_popular_advertisements(
    db: Session,
    limit: int,
    offset: int = 0,
    only_visible: bool = True,
):
    query = db.query(models.Advertisement)
    if only_visible:
        date = datetime.now()
        query = query.filter(models.Advertisement.date_start <= date)

    return (
        query.order_by(models.Advertisement.views.desc(), models.Advertisement.id)
        .offset(offset)
        .limit(limit)
    )


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_popular_advertisements_in_category(
    db: Session,
    category: models.Category,
    limit: int,
    offset: int = 0,
    only_visible: bool = True,
):
    query = db.query(models.Advertisement).filter(
        models.Advertisement.category_id == category.id
    )
    if only_visible:
        date = datetime.now()
        query = query.filter(models.Advertisement.date_start <= date)

    return (
        query.order_by(models.Advertisement.views.desc(), models.Advertisement.id)
        .offset(offset)
        .limit(limit)
    )


def get_advertisements_in_category(
    db: Session,
    category: models.Category,
    limit: int,
    offset: int = 0,
    only_visible: bool = True,
):
    query = db.query(models.Advertisement).filter(
        models.Advertisement.category_id == category.id
    )
    if only_visible:
        date = datetime.now()
        query = query.filter(models.Advertisement.date_start <= date)

    return (
        query.order_by(models.Advertisement.date_start.desc(), models.Advertisement.id)
        .offset(offset)
        .limit(limit)
    )


def create_category(db: Session, category: schemas.CategoryCreate):
    extra_fields = {}
    if category.parent is not None:
        parent = get_category_by_name(db, category.parent)
        if parent is None:
            raise RequestValidationError(
                [ErrorWrapper(ValueError("Invalid parent category"), loc="parent")]
            )
        extra_fields["parent_id"] = parent.id

    db_category = models.Category(**category.dict(exclude={"parent"}), **extra_fields)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


def serialize_advertisement(
    advertisement: models.Advertisement,
) -> schemas.AdvertisementModel:
    if advertisement.category is not None:
        advertisement.__dict__["category"] = advertisement.category.name
    return schemas.AdvertisementModel.from_orm(advertisement)


def serialize_category(category: models.Category) -> schemas.CategoryModel:
    if category.parent is not None:
        category.__dict__["parent"] = category.parent.name
    return schemas.CategoryModel.from_orm(category)
