from pydantic import BaseModel

class AdvertisementEvent(BaseModel):
    advertisement_id: int
    owner_id: int
    type: str