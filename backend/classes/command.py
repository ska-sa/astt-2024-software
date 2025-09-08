from dataclasses import dataclass
from pydantic import BaseModel
from datetime import datetime

class CreateCommand(BaseModel):
    user_id: str
    telescope_id: str
    target_az_angle: float
    target_el_angle: float

class Command(CreateCommand):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
