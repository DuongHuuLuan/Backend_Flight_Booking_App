from abc import ABC, abstractmethod
from app.domain.entities.user_entity import UserEntity


class AbstractUserRepository(ABC):

    @abstractmethod
    async def create(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None: ...

    @abstractmethod
    async def get_by_phone(self, phone: str) -> UserEntity | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserEntity | None: ...

    @abstractmethod
    async def update_password(self, user_id: int, new_password: str) -> None: ...