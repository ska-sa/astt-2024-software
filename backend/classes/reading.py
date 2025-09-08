from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel

class CreateReading(BaseModel):
    telescope_id: int
    az_angle: float
    el_angle: float
    health_status: str
    movement_status: str

class Reading(CreateReading):
    id: int
    created_at: datetime

    class Config:
        from_attribute = True

    
    