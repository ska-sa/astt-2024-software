from datetime import datetime
from pydantic import BaseModel

class Telescope(BaseModel):
    id: int
    name: str
    health_status: str #status
    created_at: datetime
