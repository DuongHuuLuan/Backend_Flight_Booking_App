from app.application.dto.booking_dto import BookingResponse
from app.domain.repositories.booking_repository import AbstractBookingRepository


class GetBookingUseCase:
    def __init__(self, booking_repo: AbstractBookingRepository):
        self.booking_repo = booking_repo

    async def execute(self, booking_id: str, user_id: int) -> BookingResponse:
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        if booking.user_id != user_id:
            raise ValueError("Booking not found")
        return BookingResponse(
            id=booking.id,
            flightId=booking.flight_id,
            totalPrice=booking.total_price,
            status=booking.status,
            createdAt=booking.created_at,
            selectedSeats=booking.selected_seat,
            zonePriceTotal=booking.zone_price_total,
            serviceTotal=booking.service_total,
            baggageTotal=booking.baggage_total,
        )
