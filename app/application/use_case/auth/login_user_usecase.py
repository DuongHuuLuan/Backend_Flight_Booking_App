from dataclasses import dataclass
from app.domain.entities.user_entity import UserEntity
from app.domain.repositories.user_repository import AbstractUserRepository
from app.core.security import verify_password

@dataclass
class LoginUserInput:
    email: str
    password: str
    
class LoginUserUseCase:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def execute(self, data: LoginUserInput) -> UserEntity:
        user = await self.repo.get_by_email(data.email)
        if not user:
            raise ValueError("Invalid email or password")
        if not verify_password(data.password, user.password):
            raise ValueError("Invalid email or password")
        return user


