from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.service_entity import ServiceEntity
from app.domain.repositories.service_repository import AbstractServiceRepository
from app.infrastructure.database.models.service_model import ServiceModel
from app.infrastructure.database.models.zone_service_eligibility_model import (
    ZoneServiceEligibilityModel,
)


class ServiceRepository(AbstractServiceRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_eligible_services(
        self, zone_id: str, age_group: str
    ) -> list[ServiceEntity]:
        result = await self.db.execute(
            select(ServiceModel)
            .select_from(ServiceModel)
            .join(
                ZoneServiceEligibilityModel,
                ZoneServiceEligibilityModel.service_id == ServiceModel.id,
            )
            .where(
                ZoneServiceEligibilityModel.zone_id == zone_id,
                ZoneServiceEligibilityModel.age_group == age_group,
                ServiceModel.is_active == True,
            )
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def get_all_services(self) -> list[ServiceEntity]:
        result = await self.db.execute(
            select(ServiceModel).where(ServiceModel.is_active == True)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def get_eligible_baggage(self) -> list[ServiceEntity]:
        result = await self.db.execute(
            select(ServiceModel).where(
                ServiceModel.type == "baggage",
                ServiceModel.is_active == True,
            )
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, m) -> ServiceEntity:
        return ServiceEntity(
            id=m.id,
            type=m.type,
            name=m.name,
            description=m.description or "",
            price=m.price,
            max_per_passenger=m.max_per_passenger or 1,
            is_active=m.is_active,
        )
