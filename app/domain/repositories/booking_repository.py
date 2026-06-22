from abc import ABC, abstractmethod

from app.domain.entities.booking_entity import BookingEntity


class AbstractBookingRepository(ABC):
    @abstractmethod
    async def create(self, booking: BookingEntity) -> BookingEntity: ...