from app.application.dto.flight_dto import (
    FlightDetailResponse, AirlineResponse, AirportResponse, CabinClassOption,
)
from app.domain.repositories.flight_repository import AbstractFlightRepository


class GetFlightDetailUseCase:
    def __init__(self, repo: AbstractFlightRepository):
        self.repo = repo

    async def execute(self, flight_id: str) -> FlightDetailResponse | None:
        flight = await self.repo.get_by_id(flight_id)
        if flight is None:
            return None

        prices = self._compute_cabin_classes(flight.price)

        return FlightDetailResponse(
            id=flight.id,
            airline=AirlineResponse(
                id=flight.airline.id,
                name=flight.airline.name,
                logoUrl=flight.airline.logo_url,
            ),
            flightNumber=flight.flight_number,
            departureAirport=AirportResponse(
                code=flight.departure_airport.code,
                name=flight.departure_airport.name,
                city=flight.departure_airport.city,
                country=flight.departure_airport.country,
            ),
            arrivalAirport=AirportResponse(
                code=flight.arrival_airport.code,
                name=flight.arrival_airport.name,
                city=flight.arrival_airport.city,
                country=flight.arrival_airport.country,
            ),
            departureTime=flight.departure_time,
            arrivalTime=flight.arrival_time,
            duration=flight.duration_minutes,
            stops=flight.stops,
            cabinClasses=prices,
        )

    def _compute_cabin_classes(self, base_price: float) -> list[CabinClassOption]:
        return [
            CabinClassOption(
                cabinClass="economy",
                price=round(base_price * 1.0, 2),
                amenities=["In-flight entertainment", "Meals & drinks", "30kg baggage"],
            ),
            CabinClassOption(
                cabinClass="business",
                price=round(base_price * 1.5, 2),
                amenities=["Priority boarding", "Lie-flat seat", "Gourmet meals",
                           "40kg baggage", "Lounge access"],
            ),
            CabinClassOption(
                cabinClass="first",
                price=round(base_price * 2.5, 2),
                amenities=["Private suite", "Chauffeur service", "Fine dining",
                           "50kg baggage", "First-class lounge", "Spa access"],
            ),
        ]