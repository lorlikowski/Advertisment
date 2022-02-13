from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from pydantic import BaseModel
import utils
from fastapi.middleware.cors import CORSMiddleware



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

JWT_EXPIRATION = timedelta(days=2)


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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Settings(BaseModel):
    authjwt_algorithm: str = "RS512"
    authjwt_public_key: str = open("RS512.key.pub", "r").read()
    authjwt_private_key: str = open("RS512.key", "r").read()

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = crud.get_user_by_email(db, email=user.email)
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Such user does not exist")
    
    if not utils.check_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Bad password")

    access_token = Authorize.create_access_token(subject=db_user.id, expires_time=JWT_EXPIRATION)

    return {"id": str(db_user.id), "key": access_token}

@app.post("/change_data", response_model=schemas.User)
def change_data(user: schemas.UserChange, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    if not utils.check_change_user(db, current_user, user):
        raise HTTPException(status_code=400, detail="Not valid data")

    db_user = crud.get_user(db, current_user)

    return crud.update_user(db, db_user, user)

@app.get("/public_data/{user_id}", response_model=schemas.UserPublic)
def public_data(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with such id does not exist")
    return db_user

@app.get("/mail/{user_id}")
def get_mail(user_id: int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with such id does not exist")
    return {"email": db_user.email}

