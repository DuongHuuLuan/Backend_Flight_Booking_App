from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.flight_entity import FlightEntity
from app.domain.entities.flight_search_params import FlightSearchParams
from app.domain.repositories.flight_repository import AbstractFlightRepository
from app.infrastructure.database.mappers.flight_mapper import FlightMapper
from app.infrastructure.database.models.flight_model import FlightModel


class FlightRepository(AbstractFlightRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_popular(self) -> list[FlightEntity]:
        result = await self.db.execute(
            select(FlightModel)
            .options(
                selectinload(FlightModel.airline),
                selectinload(FlightModel.departure_airport),
                selectinload(FlightModel.arrival_airport),
            )
            .limit(10)
        )
        return [FlightMapper.to_entity(m) for m in result.scalars().all()]

    async def search(self, params: FlightSearchParams) -> list[FlightEntity]:
        result = await self.db.execute(
            select(FlightModel)
            .options(
                selectinload(FlightModel.airline),
                selectinload(FlightModel.departure_airport),
                selectinload(FlightModel.arrival_airport),
            )
            .where(FlightModel.departure_airport_code == params.origin)
            .where(FlightModel.arrival_airport_code == params.destination)
        )
        return [FlightMapper.to_entity(m) for m in result.scalars().all()]

    async def get_all(self) -> list[FlightEntity]:
        result = await self.db.execute(
            select(FlightModel)
            .options(
                selectinload(FlightModel.airline),
                selectinload(FlightModel.departure_airport),
                selectinload(FlightModel.arrival_airport),
            )
        )
        return [FlightMapper.to_entity(m) for m in result.scalars().all()]

    async def get_by_id(self, flight_id: str) -> FlightEntity | None:
        result = await self.db.execute(
            select(FlightModel)
            .options(
                selectinload(FlightModel.airline),
                selectinload(FlightModel.departure_airport),
                selectinload(FlightModel.arrival_airport),
            )
            .where(FlightModel.id == flight_id)
        )
        model = result.scalar_one_or_none()
        return FlightMapper.to_entity(model) if model else None