from dataclasses import dataclass
from app.domain.entities.seat_zone_entity import SeatZoneEntity


@dataclass
class SeatEntity:
    id: str
    flight_id: str
    seat_label: str
    cabin_class: str
    row_number: int
    position: int
    is_available: bool
    zone: SeatZoneEntity | None = None