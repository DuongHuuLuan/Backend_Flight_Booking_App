from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.domain.entities.seat_entity import SeatEntity
from app.domain.repositories.seat_repository import AbstractSeatRepository
from app.infrastructure.database.mappers.seat_mapper import SeatMapper
from app.infrastructure.database.models.seat_model import SeatModel
from app.infrastructure.database.models.booking_model import BookingModel


class SeatRepository(AbstractSeatRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_flight(self, flight_id: str) -> list[SeatEntity]:
        result = await self.db.execute(
            select(SeatModel)
            .options(joinedload(SeatModel.zone))
            .where(SeatModel.flight_id == flight_id)
        )
        seats = result.unique().scalars().all()

        booked = await self.db.execute(
            select(BookingModel.selected_seat).where(
                BookingModel.flight_id == flight_id,
                BookingModel.selected_seat.isnot(None),
            )
        )
        reserved_labels: set[str] = set()
        for row in booked.all():
            if row[0]:
                reserved_labels.update(row[0].split(","))

        return [
            self._to_entity_with_status(s, reserved_labels) for s in seats
        ]

    async def get_by_flight_with_zones(self, flight_id: str) -> list[SeatEntity]:
        return await self.get_by_flight(flight_id)

    async def update_status(self, seat_id: str, booking_id: str):
        pass

    def _to_entity_with_status(
        self, s: SeatModel, reserved_labels: set[str]
    ) -> SeatEntity:
        entity = SeatMapper.to_entity(s)
        is_reserved = s.seat_label in reserved_labels
        entity.status = "reserved" if is_reserved else "available"
        entity.is_available = not is_reserved
        return entity
