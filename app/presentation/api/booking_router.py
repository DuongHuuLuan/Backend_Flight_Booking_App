from fastapi import APIRouter, Depends, HTTPException, status
from app.shared.dependencies import (
    get_create_booking_usecase, get_get_booking_usecase, get_current_user_id,
)
from app.application.use_case.booking.create_booking_usecase import CreateBookingUseCase
from app.application.use_case.booking.get_booking_usecase import GetBookingUseCase
from app.application.dto.booking_dto import CreateBookingRequest, BookingResponse
from app.application.dto.common import BaseResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BaseResponse[BookingResponse])
async def create_booking(
    body: CreateBookingRequest,
    user_id: int = Depends(get_current_user_id),
    uc: CreateBookingUseCase = Depends(get_create_booking_usecase),
):
    try:
        result = await uc.execute(user_id, body)
        return BaseResponse(data=result, message="Booking confirmed", success=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{booking_id}", response_model=BaseResponse[BookingResponse])
async def get_booking(
    booking_id: str,
    user_id: int = Depends(get_current_user_id),
    uc: GetBookingUseCase = Depends(get_get_booking_usecase),
):
    try:
        result = await uc.execute(booking_id, user_id)
        return BaseResponse(data=result, success=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))