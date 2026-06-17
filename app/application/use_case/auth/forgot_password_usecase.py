from dataclasses import dataclass
from app.domain.repositories.user_repository import AbstractUserRepository


class ForgotPasswordUseCase:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def execute_by_email(self, email: str) -> str:
        user = await self.repo.get_by_email(email)
        if not user:
            raise ValueError("Email not found")
        return "OTP sent to email"

    async def execute_by_sms(self, phone: str) -> str:
        user = await self.repo.get_by_phone(phone)
        if not user:
            raise ValueError("Phone not found")
        # TODO: generate OTP + send SMS
        return "OTP sent to phone"