from app.application.dto.passenger_dto import (
    UpdatePassengerRequest,
    PassengerResponse,
)
from app.domain.repositories.passenger_repository import AbstractPassengerRepository
from app.domain.repositories.booking_repository import AbstractBookingRepository


class UpdatePassengerUseCase:
    def __init__(
        self,
        passenger_repo: AbstractPassengerRepository,
        booking_repo: AbstractBookingRepository,
    ):
        self.passenger_repo = passenger_repo
        self.booking_repo = booking_repo

    async def execute(
        self, booking_id: str, passenger_id: str, user_id: int, request: UpdatePassengerRequest
    ) -> PassengerResponse:
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking is None or booking.user_id != user_id:
            raise ValueError("Booking not found")

        update_data = request.model_dump(exclude_none=True)
        passenger = await self.passenger_repo.update(passenger_id, update_data)

        return PassengerResponse(
            id=passenger.id,
            bookingId=passenger.booking_id,
            name=passenger.name,
            mobilePhone=passenger.mobile_phone,
            dateOfBirth=passenger.date_of_birth,
            passportNumber=passenger.passport_number,
            nationality=passenger.nationality,
            createdAt=passenger.created_at,
            seatLabel=passenger.seat_label,
            ageGroup=passenger.age_group,
            address=passenger.address,
            email=passenger.email,
            idNumber=passenger.id_number,
            baggageLevel=passenger.baggage_level or "none",
        )
