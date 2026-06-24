from fastapi import APIRouter, Depends
from app.application.dto.passenger_dto import (
    CreatePassengersRequest,
    PassengerResponse,
)
from app.application.dto.common import BaseResponse
from app.application.use_case.passenger.create_passengers_usecase import (
    CreatePassengersUseCase,
)
from app.shared.dependencies import (
    get_current_user_id,
    get_create_passengers_usecase,
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
