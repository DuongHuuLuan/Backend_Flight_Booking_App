from abc import ABC, abstractmethod
from app.domain.entities.service_entity import ServiceEntity


class AbstractServiceRepository(ABC):
    @abstractmethod
    async def get_eligible_services(
        self, zone_id: str, age_group: str
    ) -> list[ServiceEntity]: ...

    @abstractmethod
    async def get_all_services(self) -> list[ServiceEntity]: ...

    @abstractmethod
    async def get_eligible_baggage(self) -> list[ServiceEntity]: ...
