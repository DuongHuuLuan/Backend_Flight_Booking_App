from dataclasses import dataclass
from app.domain.repositories.user_repository import AbstractUserRepository
from app.core.security import hash_password


class ResetPasswordUseCase:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def execute_by_email(self, email: str, new_password: str) -> str:
        user = await self.repo.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        hashed = hash_password(new_password)
        await self.repo.update_password(user.id, hashed)
        return "Password updated successfully"

    async def execute_by_sms(self, phone: str, new_password: str) -> str:
        user = await self.repo.get_by_phone(phone)
        if not user:
            raise ValueError("User not found")
        hashed = hash_password(new_password)
        await self.repo.update_password(user.id, hashed)
        return "Password updated successfully"