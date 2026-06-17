from app.domain.repositories.location_repository import AbstractLocationRepository

class GetCitiesUseCase:
    def __init__(self, repo: AbstractLocationRepository):
        self.repo = repo

    async def execute(self, country: str) -> list[str]:
        return await self.repo.get_cities(country)