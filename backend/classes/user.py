from datetime import datetime

class User:
    def __init__(self, id: int, email: str, password: str, created_at: datetime) -> None:
        self.id: int = id
        self.email: str = email
        self.password: str = password
        created_at: datetime = created_at

        