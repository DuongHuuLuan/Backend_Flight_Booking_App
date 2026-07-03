from app.application.dto.booking_dto import (
    PriceBreakdownResponse,
    ZonePriceItem,
)
from app.domain.repositories.booking_repository import AbstractBookingRepository
from app.domain.repositories.flight_repository import AbstractFlightRepository
from app.domain.repositories.seat_repository import AbstractSeatRepository


class CalculatePriceUseCase:
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

        selected_labels = set()
        if booking.selected_seat:
            selected_labels = {s.strip() for s in booking.selected_seat.split(",")}

        all_seats = await self.seat_repo.get_by_flight_with_zones(flight.id)
        selected_seats = [s for s in all_seats if s.seat_label in selected_labels]

        base_fare = flight.price * len(selected_seats)

        zone_details = {}
        for seat in selected_seats:
            if seat.zone:
                zone_name = seat.zone.name
                if zone_name not in zone_details:
                    zone_details[zone_name] = {
                        "zoneName": zone_name,
                        "seatCount": 0,
                        "pricePerSeat": round(flight.price * seat.zone.price_modifier, 2),
                        "subtotal": 0.0,
                    }
                zone_details[zone_name]["seatCount"] += 1
                zone_details[zone_name]["subtotal"] += zone_details[zone_name]["pricePerSeat"]

        zone_surcharge_total = round(
            sum(d["subtotal"] for d in zone_details.values()), 2
        )

        grand_total = round(
            zone_surcharge_total + booking.service_total + booking.baggage_total,
            2,
        )

        return PriceBreakdownResponse(
            baseFare=base_fare,
            zoneSurchargeTotal=zone_surcharge_total,
            zoneDetails=[ZonePriceItem(**d) for d in zone_details.values()],
            serviceTotal=booking.service_total,
            baggageTotal=booking.baggage_total,
            grandTotal=grand_total,
        )
