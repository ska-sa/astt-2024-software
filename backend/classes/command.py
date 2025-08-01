from pydantic import BaseModel
from datetime import datetime

class Command(BaseModel):
    id: int
    user_id: int
    telescope_id: str
    target_az_angle: float #int
    target_el_angle: float #int
    created_at: datetime
