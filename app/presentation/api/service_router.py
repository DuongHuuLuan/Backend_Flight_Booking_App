from fastapi import APIRouter, Depends, Query
from app.application.dto.service_dto import EligibleServicesResponse, ServiceLimitResponse
from app.application.dto.common import BaseResponse
from app.application.use_case.service.get_eligible_services_usecase import (
    GetEligibleServicesUseCase,
)
from app.application.use_case.service.get_service_limits_usecase import (
    GetServiceLimitsUseCase,
)
from app.shared.dependencies import (
    get_eligible_services_usecase,
    get_service_limits_usecase,
)

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/eligible", response_model=BaseResponse[EligibleServicesResponse])
async def get_eligible_services(
    flight_id: str = Query(..., description="Flight ID"),
    zone_id: str = Query(..., description="Seat zone ID"),
    age_group: str = Query(..., description="Age group: child/adult/senior"),
    uc: GetEligibleServicesUseCase = Depends(get_eligible_services_usecase),
):
    result = await uc.execute(zone_id, age_group)
    return BaseResponse(data=result, success=True)


@router.get("/limits", response_model=BaseResponse[list[ServiceLimitResponse]])
async def get_service_limits(
    uc: GetServiceLimitsUseCase = Depends(get_service_limits_usecase),
):
    result = await uc.execute()
    return BaseResponse(data=result, success=True)
