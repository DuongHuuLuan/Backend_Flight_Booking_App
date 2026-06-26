from app.application.dto.seat_zone_dto import (
    FlightSeatLayoutResponse,
    SeatZoneResponse,
)
from app.domain.repositories.seat_zone_repository import AbstractSeatZoneRepository
from app.domain.repositories.seat_repository import AbstractSeatRepository


class GetSeatZonesUseCase:
    def __init__(
        self,
        zone_repo: AbstractSeatZoneRepository,
        seat_repo: AbstractSeatRepository,
    ):
        self.zone_repo = zone_repo
        self.seat_repo = seat_repo

    async def execute(self, flight_id: str) -> FlightSeatLayoutResponse:
        zones = await self.zone_repo.get_all()
        seats = await self.seat_repo.get_by_flight_with_zones(flight_id)

        zone_data = []
        for zone in zones:
            zone_seats = [s for s in seats if s.zone and s.zone.id == zone.id]
            total = len(zone_seats)
            available = sum(1 for s in zone_seats if s.is_available)
            base_price = next(
                (s.zone.price_modifier for s in zone_seats if s.zone),
                1.0,
            )
            price_per_seat = round(base_price * 100000, 0)

            zone_data.append(SeatZoneResponse(
                id=zone.id,
                name=zone.name,
                priceModifier=zone.price_modifier,
                description=zone.description,
                colorHex=zone.color_hex,
                seatCount=total,
                availableSeatCount=available,
                pricePerSeat=price_per_seat,
            ))

        return FlightSeatLayoutResponse(zones=zone_data)
