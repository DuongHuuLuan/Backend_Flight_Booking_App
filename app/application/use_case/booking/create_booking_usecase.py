import uuid
from datetime import datetime
from app.application.dto.booking_dto import CreateBookingRequest, BookingResponse
from app.domain.entities.booking_entity import BookingEntity
from app.domain.repositories.booking_repository import AbstractBookingRepository
from app.domain.repositories.flight_repository import AbstractFlightRepository


class CreateBookingUseCase:
    CABIN_MULTIPLIERS = {
        "economy": 1.0,
        "business": 1.5,
        "first": 2.5,
    }
    def __init__(
        self,
        booking_repo: AbstractBookingRepository,
        flight_repo: AbstractFlightRepository,
    ):
        self.booking_repo = booking_repo
        self.flight_repo = flight_repo

    async def execute(
        self, user_id: int, request: CreateBookingRequest
    ) -> BookingResponse:
        flight = await self.flight_repo.get_by_id(request.flight_id)
        if flight is None:
            raise ValueError("Flight not found")

        multiplier = self.CABIN_MULTIPLIERS.get(request.cabin_class, 1.0)
        total_price = round(flight.price * multiplier, 2)

        now = datetime.utcnow()
        entity = BookingEntity(
            id=str(uuid.uuid4()),
            user_id=user_id,
            flight_id=request.flight_id,
            cabin_class=request.cabin_class,
            total_price=total_price,
            status="confirmed",
            created_at=now,
            selected_seat=request.seat_label
        )
        created = await self.booking_repo.create(entity)
        if request.seat_label:
            await self.booking_repo.update_seat(created.id, request.seat_label)
        return BookingResponse(
            id=created.id,
            flightId=created.flight_id,
            cabinClass=created.cabin_class,
            totalPrice=created.total_price,
            status=created.status,
            createdAt=created.created_at,
            selectedSeat=created.selected_seat
        )