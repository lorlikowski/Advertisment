from sqlalchemy.orm.session import Session
import bcrypt
from sqlalchemy.orm import Session
from sql_app import schemas, crud

def check_password(password: str, db_password: str):
    return bcrypt.checkpw(password=password.encode(), hashed_password=db_password)

def check_change_user(db: Session, user_id: int, user: schemas.UserChange):
    db_user = crud.get_user_by_email(db, user.email)
    if (db_user and db_user.id != user_id) or user.password != user.password1:
        return False
    else:
        return True