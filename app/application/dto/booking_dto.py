from datetime import datetime
from pydantic import BaseModel


class CreateBookingRequest(BaseModel):
    flight_id: str
    cabin_class: str
    seat_labels: list[str]


class BookingResponse(BaseModel):
    id: str
    flightId: str
    cabinClass: str
    totalPrice: float
    status: str
    selectedSeats: str | None = None
    createdAt: datetime