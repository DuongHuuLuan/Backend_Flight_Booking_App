import uuid
import random
from app.application.dto.booking_dto import MockPaymentRequest, MockPaymentResponse
from app.domain.repositories.booking_repository import AbstractBookingRepository


class MockPaymentUseCase:
    def __init__(self, booking_repo: AbstractBookingRepository):
        self.booking_repo = booking_repo

    async def execute(
        self, booking_id: str, user_id: int, request: MockPaymentRequest
    ) -> MockPaymentResponse:
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking is None or booking.user_id != user_id:
            raise ValueError("Booking not found")

        if booking.status == "paid":
            return MockPaymentResponse(
                success=True,
                transactionId=booking.selected_seat,
                message="Booking already paid",
            )

        success = random.random() < 0.8

        if success:
            transaction_id = str(uuid.uuid4())[:12].upper()
            await self.booking_repo.update_status(booking_id, "paid")
            return MockPaymentResponse(
                success=True,
                transactionId=transaction_id,
                message="Payment successful",
            )
        else:
            return MockPaymentResponse(
                success=False,
                message="Payment failed. Please try again.",
            )
