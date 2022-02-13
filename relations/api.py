from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class AuthJWTSettings(BaseSettings):
    authjwt_algorithm: str = "RS512"
    authjwt_public_key: str = open("RS512.key.pub", "r").read()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

@AuthJWT.load_config
def get_config():
    return AuthJWTSettings()

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


@app.post("/add", response_model=schemas.Relation)
def add_relation(relation: schemas.RelationCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    db_relation = crud.get_relation(db, relation)
    if db_relation or user_id != relation.user_id:
        raise HTTPException(status_code=400, detail="Such relation already exists")
    return crud.create_relation(db, relation)


@app.get("/followers/{type}/{object_id}")
def get_user_followers(object_id: int, type: str, db: Session = Depends(get_db)):
    return crud.get_followers(db, type, object_id)

@app.get("/following/{type}/{user_id}")
def get_following(type: str, user_id: int, db: Session = Depends(get_db)):
    return crud.get_following(db, type, user_id)



