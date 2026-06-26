from app.application.dto.service_dto import ServiceLimitResponse


class GetServiceLimitsUseCase:
    async def execute(self) -> list[ServiceLimitResponse]:
        return [
            ServiceLimitResponse(serviceType="meal", maxQuantity=1, limitType="per_passenger"),
            ServiceLimitResponse(serviceType="drink", maxQuantity=2, limitType="per_passenger"),
            ServiceLimitResponse(serviceType="baggage", maxQuantity=1, limitType="per_passenger"),
        ]
