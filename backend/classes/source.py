from datetime import datetime
from pydantic import BaseModel

class CreateSource(BaseModel):
    source_name: str
    initial_right_ascension: float
    initial_declination: float
    rate_right_ascension: float
    rate_declination: float
    reset_period: float

class Source(CreateSource):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
