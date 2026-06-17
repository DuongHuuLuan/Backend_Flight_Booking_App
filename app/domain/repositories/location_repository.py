from abc import ABC, abstractmethod

class AbstractLocationRepository(ABC):

    @abstractmethod
    async def get_countries(self) -> list[str]: ...

    @abstractmethod
    async def get_cities(self, country: str) -> list[str]: ...