from pydantic import BaseModel

class SeatResponse(BaseModel):
    seatLabel: str
    cabinClass: str
    rowNumber: int
    position: int
    status: str  # "available" | "reserved"

class SelectSeatRequest(BaseModel):
    seat_label: str