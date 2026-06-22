from dataclasses import dataclass
from datetime import datetime


@dataclass
class BookingEntity:
    id: str
    user_id: int
    flight_id: str
    cabin_class: str
    total_price: float
    status: str
    created_at: datetime