from pydantic import BaseModel


class SeatResponse(BaseModel):
    seatLabel: str
    cabinClass: str
    rowNumber: int
    position: int
    status: str
    zoneId: str | None = None
    zoneName: str | None = None
    zonePrice: float | None = None


class SelectSeatRequest(BaseModel):
    seat_label: str