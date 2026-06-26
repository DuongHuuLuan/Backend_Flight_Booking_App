from abc import ABC, abstractmethod
from app.domain.entities.seat_zone_entity import SeatZoneEntity


class AbstractSeatZoneRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[SeatZoneEntity]: ...

    @abstractmethod
    async def get_by_id(self, zone_id: str) -> SeatZoneEntity | None: ...
