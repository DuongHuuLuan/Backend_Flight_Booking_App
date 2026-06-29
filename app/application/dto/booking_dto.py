from datetime import datetime
from pydantic import BaseModel
from app.application.dto.seat_zone_dto import SeatInput


class CreateBookingRequest(BaseModel):
    flight_id: str
    seats: list[SeatInput]


class BookingResponse(BaseModel):
    id: str
    flightId: str
    totalPrice: float
    status: str
    selectedSeats: str | None = None
    createdAt: datetime
    zonePriceTotal: float = 0
    serviceTotal: float = 0
    baggageTotal: float = 0


class ZonePriceItem(BaseModel):
    zoneName: str
    seatCount: int
    pricePerSeat: float
    subtotal: float


class PriceBreakdownResponse(BaseModel):
    baseFare: float
    zoneSurchargeTotal: float
    zoneDetails: list[ZonePriceItem]
    serviceTotal: float
    baggageTotal: float
    grandTotal: float


class MockPaymentRequest(BaseModel):
    payment_method: str = "credit_card"


class MockPaymentResponse(BaseModel):
    success: bool
    transactionId: str | None = None
    message: str
