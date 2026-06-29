from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.seat_zone_entity import SeatZoneEntity
from app.domain.repositories.seat_zone_repository import AbstractSeatZoneRepository
from app.infrastructure.database.models.seat_zone_model import SeatZoneModel


class SeatZoneRepository(AbstractSeatZoneRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[SeatZoneEntity]:
        result = await self.db.execute(select(SeatZoneModel))
        models = result.scalars().all()
        return [
            SeatZoneEntity(
                id=m.id,
                name=m.name,
                price_modifier=m.price_modifier,
                description=m.description or "",
                color_hex=m.color_hex or "",
            )
            for m in models
        ]

    async def get_by_id(self, zone_id: str) -> SeatZoneEntity | None:
        result = await self.db.execute(
            select(SeatZoneModel).where(SeatZoneModel.id == zone_id)
        )
        m = result.scalar_one_or_none()
        if m is None:
            return None
        return SeatZoneEntity(
            id=m.id,
            name=m.name,
            price_modifier=m.price_modifier,
            description=m.description or "",
            color_hex=m.color_hex or "",
        )
