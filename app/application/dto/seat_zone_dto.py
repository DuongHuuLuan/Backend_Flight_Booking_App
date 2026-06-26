from pydantic import BaseModel


class SeatZoneResponse(BaseModel):
    id: str
    name: str
    priceModifier: float
    description: str
    colorHex: str
    seatCount: int
    availableSeatCount: int
    pricePerSeat: float


class FlightSeatLayoutResponse(BaseModel):
    zones: list[SeatZoneResponse]


class SeatInput(BaseModel):
    seat_label: str
    zone_id: str
