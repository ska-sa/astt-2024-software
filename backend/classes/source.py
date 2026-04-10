from datetime import datetime
from pydantic import BaseModel

class CreateSource(BaseModel):
    source_name: str
    initial_RightAscension: float
    initial_Declination: float
    rate_RightAscension: float
    rate_Declination: float
    reset_period: float

class Source(CreateSource):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
