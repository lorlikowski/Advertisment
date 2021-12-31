from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

@app.post("/add/{user_id}/{object_id}/{type}")
def add_relation(user_id: int, object_id: int, type: str):
    return {"user_id": user_id}


@app.get("/relations/{user_id}")
def get_user_followers(user_id: int):
    return {"user_id": user_id}

@app.get("/relations/{type}/user_id")
def get_following(type: str, user_id: int):
    return {"user_id": user_id}

