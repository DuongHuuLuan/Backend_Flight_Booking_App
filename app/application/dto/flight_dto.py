from datetime import datetime
from pydantic import BaseModel


class AirportResponse(BaseModel):
    code: str
    name: str
    city: str
    country: str


class AirlineResponse(BaseModel):
    id: str
    name: str
    logo_url: str


class FlightResponse(BaseModel):
    id: str
    airline: AirlineResponse
    flight_number: str
    departure_airport: AirportResponse
    arrival_airport: AirportResponse
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: float
    stops: int
    cabin_class: str


class FlightSearchRequest(BaseModel):
    trip_type: str
    origin: str
    destination: str
    departure_date: str
    return_date: str | None = None
    passengers: int = 1
    cabin_class: str = "economy"