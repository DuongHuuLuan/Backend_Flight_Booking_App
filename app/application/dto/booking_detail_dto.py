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
    seatLabel: str | None = None
    ageGroup: str | None = None
    address: str | None = None
    email: str | None = None
    idNumber: str | None = None
    baggageLevel: str = "none"


class BookingDetailResponse(BaseModel):
    id: str
    flightId: str
    totalPrice: float
    status: str
    selectedSeats: str | None = None
    createdAt: datetime
    zonePriceTotal: float = 0
    serviceTotal: float = 0
    baggageTotal: float = 0
    flight: BookingDetailFlightResponse
    passengers: list[BookingDetailPassengerResponse]
