from dataclasses import dataclass

@dataclass
class SeatEntity:
    id: str
    flight_id: str
    seat_label: str
    cabin_class: str
    row_number: int
    position: int
    is_available: bool
    status: str = "available"