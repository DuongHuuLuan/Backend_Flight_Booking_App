from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
            select(SeatModel).where(SeatModel.flight_id == flight_id)
        )
        seats = result.scalars().all()

        # Lấy danh sách ghế đã được đặt trong flight này (CSV)
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

        entities = []
        for s in seats:
            entity = SeatMapper.to_entity(s)
            entity.status = "reserved" if s.seat_label in reserved_labels else "available"
            entities.append(entity)
        return entities

    async def update_status(self, seat_id: str, booking_id: str):
        pass  