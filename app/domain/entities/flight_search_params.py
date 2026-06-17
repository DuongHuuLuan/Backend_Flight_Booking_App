from dataclasses import dataclass
from datetime import date


@dataclass
class FlightSearchParams:
    trip_type: str
    origin: str
    destination: str
    departure_date: date
    return_date: date | None
    passengers: int
    cabin_class: str