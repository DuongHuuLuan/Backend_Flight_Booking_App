from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.domain.repositories.location_repository import AbstractLocationRepository
from app.infrastructure.database.models.country_model import CountryModel
from app.infrastructure.database.models.city_model import CityModel


class LocationRepository(AbstractLocationRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_countries(self) -> list[str]:
        result = await self.db.execute(
            select(CountryModel.name).order_by(CountryModel.name)
        )
        return result.scalars().all()

    async def get_cities(self, country: str) -> list[str]:
        result = await self.db.execute(
            select(CityModel.name)
            .join(CountryModel, CityModel.country_id == CountryModel.id)
            .where(CountryModel.name == country)
            .order_by(CityModel.name)
        )
        return result.scalars().all()