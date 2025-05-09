from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    def __init__(self, id: int, email_address: str, password: str, created_at: datetime) -> None:
        self.id: int = id
        self.email_address: str = email_address
        self.password: str = password
        created_at: datetime = created_at

        