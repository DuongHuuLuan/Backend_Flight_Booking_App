import uuid
from datetime import datetime
from app.application.dto.passenger_dto import (
    CreatePassengersRequest,
    PassengerResponse,
)
from app.domain.entities.passenger_entity import PassengerEntity
from app.domain.repositories.passenger_repository import AbstractPassengerRepository
from app.domain.repositories.booking_repository import AbstractBookingRepository


class CreatePassengersUseCase:
    def __init__(
        self,
        passenger_repo: AbstractPassengerRepository,
        booking_repo: AbstractBookingRepository,
    ):
        self.passenger_repo = passenger_repo
        self.booking_repo = booking_repo

    async def execute(
        self, booking_id: str, user_id: int, request: CreatePassengersRequest
    ) -> list[PassengerResponse]:
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        if booking.user_id != user_id:
            raise ValueError("Booking not found")

        now = datetime.utcnow()
        entities = [
            PassengerEntity(
                id=str(uuid.uuid4()),
                booking_id=booking_id,
                name=d.name,
                mobile_phone=d.mobile_phone,
                date_of_birth=d.date_of_birth,
                passport_number=d.passport_number,
                nationality=d.nationality,
                created_at=now,
                seat_label=d.seat_label,
                age_group=d.age_group,
                address=d.address,
                email=d.email,
                id_number=d.id_number,
                baggage_level=d.baggage_level or "none",
            )
            for d in request.passengers
        ]
        created = await self.passenger_repo.create_batch(booking_id, entities)
        return [
            PassengerResponse(
                id=p.id,
                bookingId=p.booking_id,
                name=p.name,
                mobilePhone=p.mobile_phone,
                dateOfBirth=p.date_of_birth,
                passportNumber=p.passport_number,
                nationality=p.nationality,
                createdAt=p.created_at,
                seatLabel=p.seat_label,
                ageGroup=p.age_group,
                address=p.address,
                email=p.email,
                idNumber=p.id_number,
                baggageLevel=p.baggage_level or "none",
            )
            for p in created
        ]
