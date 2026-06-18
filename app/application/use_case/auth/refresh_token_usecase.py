from app.core.security import decode_access_token
from app.domain.entities.user_entity import UserEntity
from app.domain.repositories.user_repository import AbstractUserRepository


class RefreshTokenUseCase:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def execute(self, refresh_token: str) -> UserEntity:
        payload = decode_access_token(refresh_token)
        if payload is None or payload.get("type") != "refresh":
            raise ValueError("Invalid or expired refresh token")

        user_id = int(payload.get("sub"))
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return user