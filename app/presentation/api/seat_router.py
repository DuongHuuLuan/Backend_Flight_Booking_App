from fastapi import APIRouter, Depends
from app.application.dto.seat_dto import SeatResponse, SelectSeatRequest
from app.application.use_case.seat.get_seat_layout_usecase import GetSeatLayoutUseCase
from app.application.use_case.seat.select_seat_usecase import SelectSeatUseCase
from app.shared.dependencies import (
    get_current_user_id,
    get_seat_layout_usecase,
    get_select_seat_usecase,
)

router = APIRouter(prefix="/flights", tags=["seats"])


@router.get("/{flight_id}/seats", response_model=list[SeatResponse])
async def get_seat_layout(
    flight_id: str,
    usecase: GetSeatLayoutUseCase = Depends(get_seat_layout_usecase),
):
    seats = await usecase.execute(flight_id)
    return [
        SeatResponse(
            seatLabel=s.seat_label,
            cabinClass=s.cabin_class,
            rowNumber=s.row_number,
            position=s.position,
            status=s.status,
        )
        for s in seats
    ]


@router.patch("/bookings/{booking_id}/seat")
async def select_seat(
    booking_id: str,
    body: SelectSeatRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: SelectSeatUseCase = Depends(get_select_seat_usecase),
):
    return await usecase.execute(booking_id, user_id, body)