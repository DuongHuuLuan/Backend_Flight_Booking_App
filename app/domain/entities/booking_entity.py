from dataclasses import dataclass
from datetime import datetime


@dataclass
class BookingEntity:
    id: str
    user_id: int
    flight_id: str
    total_price: float
    status: str
    created_at: datetime
    selected_seat: str | None = None
    zone_price_total: float = 0
    service_total: float = 0
    baggage_total: float = 0