from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class AdvertisementBase(BaseModel):
    title: str
    description: str
    date_start: Optional[datetime]
    date_end: Optional[datetime]
    

