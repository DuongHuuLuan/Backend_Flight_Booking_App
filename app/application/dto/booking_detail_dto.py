from datetime import date, datetime
from pydantic import BaseModel
from app.application.dto.flight_dto import AirlineResponse, AirportResponse


class BookingDetailFlightResponse(BaseModel):
    id: str
    airline: AirlineResponse
    flightNumber: str
    departureAirport: AirportResponse
    arrivalAirport: AirportResponse
    departureTime: datetime
    arrivalTime: datetime
    duration: int
    stops: int


class BookingDetailPassengerResponse(BaseModel):
    id: str
    bookingId: str
    name: str
    passportNumber: str
    dateOfBirth: date
    mobilePhone: str
    nationality: str
    createdAt: datetime


class BookingDetailResponse(BaseModel):
    id: str
    flightId: str
    cabinClass: str
    totalPrice: float
    status: str
    selectedSeats: str | None = None
    createdAt: datetime
    flight: BookingDetailFlightResponse
    passengers: list[BookingDetailPassengerResponse]
