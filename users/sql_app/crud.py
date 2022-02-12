from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    db_user = models.User(email=user.email, password=hashed_password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: models.User, new_data: schemas.UserChange):
    if new_data.is_admin is not None:
        user.is_admin = new_data.is_admin
    user.email = new_data.email
    user.password = bcrypt.hashpw(new_data.password.encode(), bcrypt.gensalt())
    db.commit()
    db.refresh(user)
    return user

