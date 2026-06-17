from app.domain.entities.flight_entity import FlightEntity
from app.domain.entities.flight_search_params import FlightSearchParams
from app.domain.repositories.flight_repository import AbstractFlightRepository


class SearchFlightsUseCase:
    def __init__(self, repo: AbstractFlightRepository):
        self.repo = repo

    async def execute(self, params: FlightSearchParams) -> list[FlightEntity]:
        return await self.repo.search(params)