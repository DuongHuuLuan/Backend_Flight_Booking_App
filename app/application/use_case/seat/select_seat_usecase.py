from sqlalchemy import select
from app.application.dto.seat_dto import SelectSeatRequest
from app.domain.repositories.seat_repository import AbstractSeatRepository
from app.domain.repositories.booking_repository import AbstractBookingRepository


class SelectSeatUseCase:
    def __init__(
        self,
        seat_repo: AbstractSeatRepository,
        booking_repo: AbstractBookingRepository,
    ):
        self.seat_repo = seat_repo
        self.booking_repo = booking_repo

    async def execute(self, booking_id: str, user_id: int, request: SelectSeatRequest):
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        if booking.user_id != user_id:
            raise PermissionError("You do not own this booking")

        await self.booking_repo.update_seat(booking_id, request.seat_label)
        return {"message": "Seat selected successfully", "seat": request.seat_label}