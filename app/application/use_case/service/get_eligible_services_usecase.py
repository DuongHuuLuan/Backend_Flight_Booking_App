from app.application.dto.service_dto import (
    EligibleServicesResponse,
    ServiceResponse,
    ServiceLimitResponse,
)
from app.domain.repositories.service_repository import AbstractServiceRepository


class GetEligibleServicesUseCase:
    def __init__(self, service_repo: AbstractServiceRepository):
        self.service_repo = service_repo

    async def execute(
        self, zone_id: str, age_group: str
    ) -> EligibleServicesResponse:
        services = await self.service_repo.get_eligible_services(zone_id, age_group)
        all_baggage = await self.service_repo.get_eligible_baggage()

        meals = [s for s in services if s.type == "meal"]
        drinks = [s for s in services if s.type == "drink"]

        limits = [
            ServiceLimitResponse(serviceType="meal", maxQuantity=1, limitType="per_passenger"),
            ServiceLimitResponse(serviceType="drink", maxQuantity=2, limitType="per_passenger"),
            ServiceLimitResponse(serviceType="baggage", maxQuantity=1, limitType="per_passenger"),
        ]

        return EligibleServicesResponse(
            meals=[self._to_response(s) for s in meals],
            drinks=[self._to_response(s) for s in drinks],
            baggage=[self._to_response(s) for s in all_baggage],
            limits=limits,
        )

    def _to_response(self, service) -> ServiceResponse:
        return ServiceResponse(
            id=service.id,
            type=service.type,
            name=service.name,
            description=service.description or "",
            price=service.price,
            maxPerPassenger=service.max_per_passenger,
        )
