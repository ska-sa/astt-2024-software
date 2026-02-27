from datetime import datetime
from pydantic import BaseModel

class CreatePosition(BaseModel):
    datetime : datetime

class Position(CreatePosition):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True    