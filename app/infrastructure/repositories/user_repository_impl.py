from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user_entity import UserEntity
from app.domain.repositories.user_repository import AbstractUserRepository
from app.infrastructure.database.mappers.user_mapper import UserMapper
from app.infrastructure.database.models.user_model import UserModel


class UserRepository(AbstractUserRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserEntity) -> UserEntity:
        model = UserMapper.to_model(user)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        return UserMapper.to_entity(model)

    async def get_by_email(self, email: str) -> UserEntity | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    async def get_by_phone(self, phone: str) -> UserEntity | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.phone == phone)
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_entity(model) if model else None

    async def update_password(self, user_id: int, new_password: str) -> None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.password = new_password

    async def update(self, user: UserEntity) -> UserEntity:
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one_or_none()
        if model:
            UserMapper.update_model(model, user)
            return UserMapper.to_entity(model)
        raise ValueError(f"User {user.id} not found")