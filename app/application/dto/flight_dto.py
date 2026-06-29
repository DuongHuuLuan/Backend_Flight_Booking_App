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
    logoUrl: str


class FlightResponse(BaseModel):
    id: str
    airline: AirlineResponse
    flightNumber: str
    departureAirport: AirportResponse
    arrivalAirport: AirportResponse
    departureTime: datetime
    arrivalTime: datetime
    duration: int
    price: float
    stops: int


class FlightSearchRequest(BaseModel):
    trip_type: str
    origin: str
    destination: str
    departure_date: str
    return_date: str | None = None
    passengers: int = 1


class FlightDetailResponse(BaseModel):
    id: str
    airline: AirlineResponse
    flightNumber: str
    departureAirport: AirportResponse
    arrivalAirport: AirportResponse
    departureTime: datetime
    arrivalTime: datetime
    duration: int
    stops: int
    basePrice: float