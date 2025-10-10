from datetime import datetime
from pydantic import BaseModel

class CreateTelescope(BaseModel):
    name: str
    health_status: int

class Telescope(CreateTelescope):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True