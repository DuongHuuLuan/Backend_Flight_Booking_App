from fastapi import APIRouter, Depends, HTTPException, status
from app.application.dto.passenger_dto import (
    CreatePassengersRequest,
    PassengerResponse,
    UpdatePassengerRequest,
)
from app.application.dto.service_dto import AssignServicesRequest
from app.application.dto.common import BaseResponse
from app.application.use_case.passenger.create_passengers_usecase import (
    CreatePassengersUseCase,
)
from app.application.use_case.passenger.update_passenger_usecase import (
    UpdatePassengerUseCase,
)
from app.application.use_case.service.assign_services_usecase import (
    AssignServicesUseCase,
)
from app.shared.dependencies import (
    get_current_user_id,
    get_create_passengers_usecase,
    get_update_passenger_usecase,
    get_assign_services_usecase,
)

router = APIRouter(prefix="/bookings", tags=["passengers"])


@router.post(
    "/{booking_id}/passengers", response_model=BaseResponse[list[PassengerResponse]]
)
async def create_passengers(
    booking_id: str,
    body: CreatePassengersRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: CreatePassengersUseCase = Depends(get_create_passengers_usecase),
):
    result = await usecase.execute(booking_id, user_id, body)
    return BaseResponse(data=result, success=True)


@router.patch(
    "/{booking_id}/passengers/{passenger_id}",
    response_model=BaseResponse[PassengerResponse],
)
async def update_passenger(
    booking_id: str,
    passenger_id: str,
    body: UpdatePassengerRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: UpdatePassengerUseCase = Depends(get_update_passenger_usecase),
):
    try:
        result = await usecase.execute(booking_id, passenger_id, user_id, body)
        return BaseResponse(data=result, success=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{booking_id}/services",
    response_model=BaseResponse[list[PassengerResponse]],
)
async def assign_services(
    booking_id: str,
    body: AssignServicesRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: AssignServicesUseCase = Depends(get_assign_services_usecase),
):
    try:
        result = await usecase.execute(booking_id, user_id, body)
        return BaseResponse(data=result, success=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
