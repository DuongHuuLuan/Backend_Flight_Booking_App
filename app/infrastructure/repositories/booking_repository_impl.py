from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.booking_entity import BookingEntity
from app.domain.repositories.booking_repository import AbstractBookingRepository
from app.infrastructure.database.mappers.booking_mapper import BookingMapper
from app.infrastructure.database.models.booking_model import BookingModel


class BookingRepository(AbstractBookingRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def create(self, booking: BookingEntity):
        model = BookingModel(
            id=booking.id,
            user_id=booking.user_id,
            flight_id=booking.flight_id,
            cabin_class=booking.cabin_class,
            total_price=booking.total_price,
            status=booking.status,
            selected_seat=booking.selected_seat,
            created_at=booking.created_at,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return BookingMapper.to_entity(model)
    
    async def get_by_id(self, booking_id: str) -> BookingEntity | None:
        result = await self.db.execute(
            select(BookingModel).where(BookingModel.id == booking_id)
        )
        model = result.scalar_one_or_none()
        return BookingMapper.to_entity(model) if model else None

    async def update_seat(self, booking_id: str, seat_label: str) -> None:
        result = await self.db.execute(
            select(BookingModel).where(BookingModel.id == booking_id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.selected_seat = seat_label
            await self.db.commit()