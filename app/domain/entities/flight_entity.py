from datetime import datetime
from dataclasses import dataclass
from app.domain.entities.airline_entity import AirlineEntity
from app.domain.entities.airport_entity import AirportEntity


@dataclass
class FlightEntity:
    id: str
    airline: AirlineEntity
    flight_number: str
    departure_airport: AirportEntity
    arrival_airport: AirportEntity
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: float
    stops: int
    cabin_class: str