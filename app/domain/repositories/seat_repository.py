from abc import ABC, abstractmethod
from app.domain.entities.seat_entity import SeatEntity


class AbstractSeatRepository(ABC):
    @abstractmethod
    async def get_by_flight(self, flight_id: str) -> list[SeatEntity]: ...

    @abstractmethod
    async def update_status(self, seat_id: str, booking_id: str): ...

    @abstractmethod
    async def get_by_flight_with_zones(self, flight_id: str) -> list[SeatEntity]: ...