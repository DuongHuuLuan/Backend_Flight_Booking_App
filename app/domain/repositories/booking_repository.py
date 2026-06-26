from abc import ABC, abstractmethod

from app.domain.entities.booking_entity import BookingEntity


class AbstractBookingRepository(ABC):
    @abstractmethod
    async def create(self, booking: BookingEntity) -> BookingEntity: ...

    @abstractmethod
    async def get_by_id(self, booking_id: str) -> BookingEntity | None: ...

    @abstractmethod
    async def update_seat(self, booking_id: str, seat_label: str) -> None: ...

    @abstractmethod
    async def update_totals(
        self, booking_id: str,
        zone_price_total: float,
        service_total: float,
        baggage_total: float,
    ) -> None: ...

    @abstractmethod
    async def update_status(self, booking_id: str, status: str) -> None: ...