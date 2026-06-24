from abc import ABC, abstractmethod
from app.domain.entities.passenger_entity import PassengerEntity


class AbstractPassengerRepository(ABC):
    @abstractmethod
    async def create_batch(
        self, booking_id: str, passengers: list[PassengerEntity]
    ) -> list[PassengerEntity]: ...

    @abstractmethod
    async def get_by_booking_id(self, booking_id: str) -> list[PassengerEntity]: ...
