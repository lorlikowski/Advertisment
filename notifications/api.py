from fastapi import FastAPI
import schemas
from worker import send_email

app = FastAPI()


@app.post("/advertisement")
def advertisement(advertisement: schemas.AdvertisementEvent):
    task = send_email.delay(advertisement.advertisement_id, advertisement.owner_id, advertisement.type)
    return {"task_id": task.id}




