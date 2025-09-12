from dataclasses import dataclass
from pydantic import BaseModel
from datetime import datetime

class CreateCommand(BaseModel):
    user_id: int
    telescope_id: int
    target_az_angle: float
    target_el_angle: float

class Command(CreateCommand):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
