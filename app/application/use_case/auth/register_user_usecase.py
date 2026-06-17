from dataclasses import dataclass
from app.domain.entities.user_entity import UserEntity
from app.domain.repositories.user_repository import AbstractUserRepository
from app.core.security import hash_password


@dataclass
class RegisterUserInput:
    name: str
    email: str
    phone: str
    country: str
    city: str
    password: str

class RegisterUserUseCase:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def execute(self, data: RegisterUserInput) -> UserEntity:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")
        existing_phone = await self.repo.get_by_phone(data.phone)
        if existing_phone:
            raise ValueError("Phone already registered")

        user = UserEntity(
            id=None,
            name=data.name,
            email=data.email,
            phone=data.phone,
            country=data.country,
            city=data.city,
            password=hash_password(data.password),
            avatar=None,
            created_at=None,
        )
        return await self.repo.create(user)

