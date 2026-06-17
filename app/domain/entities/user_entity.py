
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    id: int 
    name: str
    email: str
    phone: str
    country: str
    city: str
    password: str
    avatar: str | None
    created_at: datetime | None