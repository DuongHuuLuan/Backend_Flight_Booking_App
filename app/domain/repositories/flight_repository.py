from abc import ABC, abstractmethod
from app.domain.entities.flight_entity import FlightEntity
from app.domain.entities.flight_search_params import FlightSearchParams


class AbstractFlightRepository(ABC):

    @abstractmethod
    async def get_popular(self) -> list[FlightEntity]: ...

    @abstractmethod
    async def search(self, params: FlightSearchParams) -> list[FlightEntity]: ...

    @abstractmethod
    async def get_all(self) -> list[FlightEntity]: ...