from datetime import datetime
from pydantic import BaseModel
#ToDo
class  Position(BaseModel):
    id: int
    created_at: datetime
    datetime: datetime
    