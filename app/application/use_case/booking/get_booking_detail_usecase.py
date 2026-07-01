from app.application.dto.booking_detail_dto import (
    BookingDetailResponse,
    BookingDetailFlightResponse,
    BookingDetailPassengerResponse,
)
from app.application.dto.flight_dto import AirlineResponse, AirportResponse
from app.domain.repositories.booking_repository import AbstractBookingRepository
from app.domain.repositories.flight_repository import AbstractFlightRepository
from app.domain.repositories.passenger_repository import AbstractPassengerRepository
from app.domain.repositories.service_repository import AbstractServiceRepository


class GetBookingDetailUseCase:
    def __init__(
        self,
        booking_repo: AbstractBookingRepository,
        flight_repo: AbstractFlightRepository,
        passenger_repo: AbstractPassengerRepository,
        service_repo: AbstractServiceRepository,
    ):
        self.booking_repo = booking_repo
        self.flight_repo = flight_repo
        self.passenger_repo = passenger_repo
        self.service_repo = service_repo

    async def execute(
        self, booking_id: str, user_id: int
    ) -> BookingDetailResponse:
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking is None or booking.user_id != user_id:
            raise ValueError("Booking not found")

        flight = await self.flight_repo.get_by_id(booking.flight_id)
        if flight is None:
            raise ValueError("Flight not found")

        passengers = await self.passenger_repo.get_by_booking_id(booking_id)
        all_services = await self.service_repo.get_all_services()
        service_name_map = {s.id: s.name for s in all_services if s.type == "baggage"}

        return BookingDetailResponse(
            id=booking.id,
            flightId=booking.flight_id,
            totalPrice=booking.total_price,
            status=booking.status,
            selectedSeats=booking.selected_seat,
            createdAt=booking.created_at,
            zonePriceTotal=booking.zone_price_total,
            serviceTotal=booking.service_total,
            baggageTotal=booking.baggage_total,
            flight=BookingDetailFlightResponse(
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
            ),
            passengers=[
                BookingDetailPassengerResponse(
                    id=p.id,
                    bookingId=p.booking_id,
                    name=p.name,
                    passportNumber=p.passport_number,
                    dateOfBirth=p.date_of_birth,
                    mobilePhone=p.mobile_phone,
                    nationality=p.nationality,
                    createdAt=p.created_at,
                    seatLabel=p.seat_label,
                    ageGroup=p.age_group,
                    address=p.address,
                    email=p.email,
                    idNumber=p.id_number,
                    baggageLevel=p.baggage_level or "none",
                    baggageName=service_name_map.get(p.baggage_level, "None") if p.baggage_level else "None",
                )
                for p in passengers
            ],
        )
