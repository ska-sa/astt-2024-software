from datetime import datetime
from pydantic import BaseModel

class Reading(BaseModel):
    id: int
    telescope_id: str
    az_angle: float
    el_angle: float
    health_status: str
    movement_status: str
    created_at: datetime
    
    