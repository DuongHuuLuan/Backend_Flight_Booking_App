from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.passenger_entity import PassengerEntity
from app.domain.repositories.passenger_repository import AbstractPassengerRepository
from app.infrastructure.database.mappers.passenger_mapper import PassengerMapper
from app.infrastructure.database.models.passenger_model import PassengerModel


class PassengerRepository(AbstractPassengerRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_batch(
        self, booking_id: str, passengers: list[PassengerEntity]
    ) -> list[PassengerEntity]:
        models = [
            PassengerModel(
                id=p.id,
                booking_id=booking_id,
                name=p.name,
                mobile_phone=p.mobile_phone,
                date_of_birth=p.date_of_birth,
                passport_number=p.passport_number,
                nationality=p.nationality,
                created_at=p.created_at,
            )
            for p in passengers
        ]
        self.db.add_all(models)
        await self.db.commit()
        for m in models:
            await self.db.refresh(m)
        return [PassengerMapper.to_entity(m) for m in models]

    async def get_by_booking_id(self, booking_id: str) -> list[PassengerEntity]:
        from sqlalchemy import select
        result = await self.db.execute(
            select(PassengerModel).where(PassengerModel.booking_id == booking_id)
        )
        models = result.scalars().all()
        return [PassengerMapper.to_entity(m) for m in models]
