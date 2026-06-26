import uuid
from datetime import datetime
from app.application.dto.booking_dto import CreateBookingRequest, BookingResponse
from app.domain.entities.booking_entity import BookingEntity
from app.domain.repositories.booking_repository import AbstractBookingRepository
from app.domain.repositories.flight_repository import AbstractFlightRepository
from app.domain.repositories.seat_zone_repository import AbstractSeatZoneRepository


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
        zone_repo: AbstractSeatZoneRepository,
    ):
        self.booking_repo = booking_repo
        self.flight_repo = flight_repo
        self.zone_repo = zone_repo

    async def execute(
        self, user_id: int, request: CreateBookingRequest
    ) -> BookingResponse:
        flight = await self.flight_repo.get_by_id(request.flight_id)
        if flight is None:
            raise ValueError("Flight not found")

        if not request.seats:
            raise ValueError("At least one seat must be selected")

        multiplier = self.CABIN_MULTIPLIERS.get(request.cabin_class, 1.0)
        base_price = flight.price * multiplier
        cabin_fare = round(base_price * len(request.seats), 2)

        seat_labels_csv = ",".join(s.seat_label for s in request.seats)

        zone_price_total = 0.0
        for seat in request.seats:
            zone = await self.zone_repo.get_by_id(seat.zone_id)
            if zone:
                zone_price_total += round(base_price * zone.price_modifier, 2)
        zone_price_total = round(zone_price_total, 2)

        total_price = round(cabin_fare + zone_price_total, 2)

        now = datetime.utcnow()
        entity = BookingEntity(
            id=str(uuid.uuid4()),
            user_id=user_id,
            flight_id=request.flight_id,
            cabin_class=request.cabin_class,
            total_price=total_price,
            status="confirmed",
            created_at=now,
            selected_seat=seat_labels_csv,
            zone_price_total=zone_price_total,
        )
        created = await self.booking_repo.create(entity)
        await self.booking_repo.update_seat(created.id, seat_labels_csv)
        return BookingResponse(
            id=created.id,
            flightId=created.flight_id,
            cabinClass=created.cabin_class,
            totalPrice=created.total_price,
            status=created.status,
            createdAt=created.created_at,
            selectedSeats=seat_labels_csv,
            zonePriceTotal=created.zone_price_total,
        )