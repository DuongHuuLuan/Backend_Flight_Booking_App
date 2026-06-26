from app.application.dto.booking_dto import (
    PriceBreakdownResponse,
    ZonePriceItem,
)
from app.domain.repositories.booking_repository import AbstractBookingRepository
from app.domain.repositories.flight_repository import AbstractFlightRepository
from app.domain.repositories.seat_repository import AbstractSeatRepository


class CalculatePriceUseCase:
    CABIN_MULTIPLIERS = {
        "economy": 1.0,
        "business": 1.5,
        "first": 2.5,
    }

    def __init__(
        self,
        booking_repo: AbstractBookingRepository,
        flight_repo: AbstractFlightRepository,
        seat_repo: AbstractSeatRepository,
    ):
        self.booking_repo = booking_repo
        self.flight_repo = flight_repo
        self.seat_repo = seat_repo

    async def execute(
        self, booking_id: str, user_id: int
    ) -> PriceBreakdownResponse:
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking is None or booking.user_id != user_id:
            raise ValueError("Booking not found")

        flight = await self.flight_repo.get_by_id(booking.flight_id)
        if flight is None:
            raise ValueError("Flight not found")

        seats = await self.seat_repo.get_by_flight_with_zones(flight.id)
        cabin_mult = self.CABIN_MULTIPLIERS.get(booking.cabin_class, 1.0)

        base_fare = flight.price
        cabin_fare = round(base_fare * cabin_mult, 2)

        zone_details = []
        zone_surcharge_total = 0.0

        for seat in seats:
            if seat.zone:
                zone_price = round(base_fare * seat.zone.price_modifier, 2)
                zone_surcharge_total += zone_price

        zone_surcharge_total = round(zone_surcharge_total, 2)

        grand_total = round(
            base_fare + cabin_fare + zone_surcharge_total
            + booking.service_total + booking.baggage_total,
            2,
        )

        return PriceBreakdownResponse(
            baseFare=base_fare,
            cabinFare=cabin_fare,
            zoneSurchargeTotal=zone_surcharge_total,
            zoneDetails=zone_details,
            serviceTotal=booking.service_total,
            baggageTotal=booking.baggage_total,
            grandTotal=grand_total,
        )
