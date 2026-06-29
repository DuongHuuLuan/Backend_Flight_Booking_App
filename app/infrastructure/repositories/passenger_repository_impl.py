from sqlalchemy import select, update as sa_update
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
                seat_label=p.seat_label,
                age_group=p.age_group,
                address=p.address,
                email=p.email,
                id_number=p.id_number,
            )
            for p in passengers
        ]
        self.db.add_all(models)
        await self.db.commit()
        for m in models:
            await self.db.refresh(m)
        return [PassengerMapper.to_entity(m) for m in models]

    async def get_by_booking_id(self, booking_id: str) -> list[PassengerEntity]:
        result = await self.db.execute(
            select(PassengerModel).where(PassengerModel.booking_id == booking_id)
        )
        models = result.scalars().all()
        return [PassengerMapper.to_entity(m) for m in models]

    async def update(
        self, passenger_id: str, data: dict
    ) -> PassengerEntity:
        allowed = {
            "name", "mobile_phone", "date_of_birth", "passport_number",
            "nationality", "address", "email", "id_number",
            "age_group", "seat_label", "baggage_level",
        }
        clean = {k: v for k, v in data.items() if k in allowed and v is not None}

        stmt = (
            sa_update(PassengerModel)
            .where(PassengerModel.id == passenger_id)
            .values(**clean)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        await self.db.commit()

        result = await self.db.execute(
            select(PassengerModel).where(PassengerModel.id == passenger_id)
        )
        return PassengerMapper.to_entity(result.scalar_one())
