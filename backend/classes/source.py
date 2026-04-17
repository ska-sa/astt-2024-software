from datetime import datetime
from pydantic import BaseModel

class CreateSource(BaseModel):
    name: str
    initial_right_ascension: float
    initial_declination: float
    right_ascension_rate: float
    declination_rate: float
    reset_period_days: int

class Source(CreateSource):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
