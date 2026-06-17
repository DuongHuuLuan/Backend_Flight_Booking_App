from app.domain.repositories.location_repository import AbstractLocationRepository


class GetCountriesUseCase:
    def __init__(self, repo: AbstractLocationRepository):
        self.repo = repo

    async def execute(self) -> list[str]:
        return await self.repo.get_countries()