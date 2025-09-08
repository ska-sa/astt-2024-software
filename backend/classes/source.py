from datetime import datetime
from pydantic import BaseModel

class CreateSource(BaseModel):
    name: str

class Source(CreateSource):
    id: int

    class Config:
        from_attributes = True