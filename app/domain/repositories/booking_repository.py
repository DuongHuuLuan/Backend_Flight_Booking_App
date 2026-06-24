from abc import ABC, abstractmethod

from app.domain.entities.booking_entity import BookingEntity


class AbstractBookingRepository(ABC):
    @abstractmethod
    async def create(self, booking: BookingEntity) -> BookingEntity: ...
    @abstractmethod
    async def get_by_id(self, booking_id: str) -> BookingEntity | None: ...
    @abstractmethod
    async def update_seat(self, booking_id: str, seat_label: str) -> None: ...