from app.domain.entities.user_entity import UserEntity
from app.domain.repositories.user_repository import AbstractUserRepository


class GetMeUseCase:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def execute(self, user_id: int) -> UserEntity:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user