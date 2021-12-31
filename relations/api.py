from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add", response_model=schemas.Relation)
def add_relation(relation: schemas.RelationCreate, db: Session = Depends(get_db)):
    db_relation = crud.get_relation(db, relation)
    if db_relation:
        raise HTTPException(status_code=400, detail="Such relation already exists")
    return crud.create_relation(db, relation)


@app.get("/relations/{user_id}")
def get_user_followers(user_id: int, db: Session = Depends(get_db)):
    return crud.get_followers(db, user_id)

@app.get("/relations/{type}/user_id")
def get_following(type: str, user_id: int, db: Session = Depends(get_db)):
    return crud.get_following(db, type, user_id)

