import uuid
from app.application.dto.passenger_dto import PassengerResponse
from app.application.dto.service_dto import AssignServicesRequest
from app.domain.repositories.passenger_repository import AbstractPassengerRepository
from app.domain.repositories.booking_repository import AbstractBookingRepository
from app.domain.repositories.service_repository import AbstractServiceRepository


class AssignServicesUseCase:
    def __init__(
        self,
        passenger_repo: AbstractPassengerRepository,
        booking_repo: AbstractBookingRepository,
        service_repo: AbstractServiceRepository,
    ):
        self.passenger_repo = passenger_repo
        self.booking_repo = booking_repo
        self.service_repo = service_repo

    async def execute(
        self, booking_id: str, user_id: int, request: AssignServicesRequest
    ) -> list[PassengerResponse]:
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking is None or booking.user_id != user_id:
            raise ValueError("Booking not found")

        all_services = await self.service_repo.get_all_services()
        service_map = {s.id: s for s in all_services}

        total_service = booking.service_total or 0.0
        total_baggage = booking.baggage_total or 0.0
        updated_passengers = []

        for passenger_input in request.passengers:
            passenger = await self.passenger_repo.update(
                passenger_input.passenger_id,
                {"baggage_level": passenger_input.baggage_level},
            )

            psngr_service_total = sum(
                service_map[sid].price for sid in passenger_input.service_ids
                if sid in service_map and service_map[sid].type != "baggage"
            )

            baggage_price = sum(
                s.price for s in all_services
                if s.type == "baggage"
                and s.id == passenger_input.baggage_level
            )

            if passenger_input.baggage_level and passenger_input.baggage_level != "none":
                total_baggage += baggage_price
            total_service += psngr_service_total

            updated_passengers.append(passenger)

        grand_total = round(
            booking.zone_price_total + total_service + total_baggage, 2
        )
        await self.booking_repo.update_totals(
            booking_id,
            zone_price_total=booking.zone_price_total,
            service_total=total_service,
            baggage_total=total_baggage,
            total_price=grand_total,
        )

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
            for p in updated_passengers
        ]
