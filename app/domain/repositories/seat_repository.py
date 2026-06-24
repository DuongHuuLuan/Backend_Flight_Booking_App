from abc import ABC
from app.domain.entities.seat_entity import SeatEntity


class AbstractSeatRepository(ABC):
    async def get_by_flight(self, flight_id: str) -> list[SeatEntity]: ...
    async def update_status(self, seat_id: str, booking_id: str): ...