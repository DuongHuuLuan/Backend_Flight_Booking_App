from datetime import datetime
from pydantic import BaseModel


class CreateBookingRequest(BaseModel):
    flight_id: str
    cabin_class: str
    seat_label: str | None = None
    
class BookingResponse(BaseModel):
    id: str
    flightId: str
    cabinClass: str
    totalPrice: float
    status: str
    selectedSeat: str | None = None
    createdAt: datetime