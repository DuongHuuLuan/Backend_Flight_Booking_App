from app.domain.entities.flight_entity import FlightEntity
from app.domain.repositories.flight_repository import AbstractFlightRepository


class GetAllFlightsUseCase:
    def __init__(self, repo: AbstractFlightRepository):
        self.repo = repo

    async def execute(self) -> list[FlightEntity]:
        return await self.repo.get_all()