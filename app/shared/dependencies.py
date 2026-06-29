from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.application.use_case.booking.create_booking_usecase import CreateBookingUseCase
from app.application.use_case.booking.get_booking_usecase import GetBookingUseCase
from app.application.use_case.booking.get_booking_detail_usecase import GetBookingDetailUseCase
from app.application.use_case.booking.calculate_price_usecase import CalculatePriceUseCase
from app.application.use_case.booking.mock_payment_usecase import MockPaymentUseCase
from app.application.use_case.flight.get_flight_detail_usecase import GetFlightDetailUseCase
from app.application.use_case.seat.get_seat_layout_usecase import GetSeatLayoutUseCase
from app.application.use_case.seat.select_seat_usecase import SelectSeatUseCase
from app.application.use_case.seat.get_seat_zones_usecase import GetSeatZonesUseCase
from app.application.use_case.service.get_eligible_services_usecase import GetEligibleServicesUseCase
from app.application.use_case.service.get_service_limits_usecase import GetServiceLimitsUseCase
from app.application.use_case.service.assign_services_usecase import AssignServicesUseCase
from app.application.use_case.passenger.update_passenger_usecase import UpdatePassengerUseCase
from app.domain.repositories.booking_repository import AbstractBookingRepository
from app.domain.repositories.seat_repository import AbstractSeatRepository
from app.domain.repositories.passenger_repository import AbstractPassengerRepository
from app.domain.repositories.seat_zone_repository import AbstractSeatZoneRepository
from app.domain.repositories.service_repository import AbstractServiceRepository
from app.infrastructure.database.session import get_db as _get_db
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException

from app.domain.repositories.user_repository import AbstractUserRepository
from app.domain.repositories.flight_repository import AbstractFlightRepository
from app.domain.repositories.location_repository import AbstractLocationRepository

from app.infrastructure.repositories.booking_repository_impl import BookingRepository
from app.infrastructure.repositories.seat_repository_impl import SeatRepository
from app.infrastructure.repositories.seat_zone_repository_impl import SeatZoneRepository
from app.infrastructure.repositories.service_repository_impl import ServiceRepository
from app.infrastructure.repositories.user_repository_impl import UserRepository
from app.infrastructure.repositories.flight_repository_impl import FlightRepository
from app.infrastructure.repositories.location_repository_impl import LocationRepository
from app.infrastructure.repositories.passenger_repository_impl import PassengerRepository
from app.application.use_case.auth.login_user_usecase import LoginUserUseCase
from app.application.use_case.auth.register_user_usecase import RegisterUserUseCase
from app.application.use_case.auth.logout_user_usecase import LogoutUserUseCase
from app.application.use_case.auth.forgot_password_usecase import ForgotPasswordUseCase
from app.application.use_case.auth.verify_otp_usecase import VerifyOtpUseCase
from app.application.use_case.auth.reset_password_usecase import ResetPasswordUseCase
from app.application.use_case.flight.get_popular_flights_usecase import GetPopularFlightsUseCase
from app.application.use_case.flight.search_flights_usecase import SearchFlightsUseCase
from app.application.use_case.flight.get_all_flights_usecase import GetAllFlightsUseCase
from app.application.use_case.location.get_countries_usecase import GetCountriesUseCase
from app.application.use_case.location.get_cities_usecase import GetCitiesUseCase
from typing import AsyncIterator
from app.application.use_case.auth.refresh_token_usecase import RefreshTokenUseCase
from app.application.use_case.auth.get_me_usecase import GetMeUseCase
from app.application.use_case.passenger.create_passengers_usecase import CreatePassengersUseCase

security_scheme = HTTPBearer()


# ── Repositories ──

async def get_db() -> AsyncIterator[AsyncSession]:
    async for session in _get_db():
        yield session


def get_user_repo(db: AsyncSession = Depends(get_db)) -> AbstractUserRepository:
    return UserRepository(db)


def get_flight_repo(db: AsyncSession = Depends(get_db)) -> AbstractFlightRepository:
    return FlightRepository(db)


def get_location_repo(db: AsyncSession = Depends(get_db)) -> AbstractLocationRepository:
    return LocationRepository(db)


def get_booking_repo(db: AsyncSession = Depends(get_db)) -> AbstractBookingRepository:
    return BookingRepository(db)


def get_seat_repo(db: AsyncSession = Depends(get_db)) -> AbstractSeatRepository:
    return SeatRepository(db)


def get_seat_zone_repo(db: AsyncSession = Depends(get_db)) -> AbstractSeatZoneRepository:
    return SeatZoneRepository(db)


def get_service_repo(db: AsyncSession = Depends(get_db)) -> AbstractServiceRepository:
    return ServiceRepository(db)


def get_passenger_repo(db: AsyncSession = Depends(get_db)) -> AbstractPassengerRepository:
    return PassengerRepository(db)


# ── Use Cases ──

def get_login_usecase(repo: AbstractUserRepository = Depends(get_user_repo)) -> LoginUserUseCase:
    return LoginUserUseCase(repo)


def get_register_usecase(repo: AbstractUserRepository = Depends(get_user_repo)) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo)


def get_logout_usecase() -> LogoutUserUseCase:
    return LogoutUserUseCase()


def get_forgot_password_usecase(
    repo: AbstractUserRepository = Depends(get_user_repo),
) -> ForgotPasswordUseCase:
    return ForgotPasswordUseCase(repo)


def get_verify_otp_usecase() -> VerifyOtpUseCase:
    return VerifyOtpUseCase()


def get_reset_password_usecase(
    repo: AbstractUserRepository = Depends(get_user_repo),
) -> ResetPasswordUseCase:
    return ResetPasswordUseCase(repo)


def get_popular_flights_usecase(
    repo: AbstractFlightRepository = Depends(get_flight_repo),
) -> GetPopularFlightsUseCase:
    return GetPopularFlightsUseCase(repo)


def get_search_flights_usecase(
    repo: AbstractFlightRepository = Depends(get_flight_repo),
) -> SearchFlightsUseCase:
    return SearchFlightsUseCase(repo)


def get_all_flights_usecase(
    repo: AbstractFlightRepository = Depends(get_flight_repo),
) -> GetAllFlightsUseCase:
    return GetAllFlightsUseCase(repo)


def get_countries_usecase(
    repo: AbstractLocationRepository = Depends(get_location_repo),
) -> GetCountriesUseCase:
    return GetCountriesUseCase(repo)


def get_cities_usecase(
    repo: AbstractLocationRepository = Depends(get_location_repo),
) -> GetCitiesUseCase:
    return GetCitiesUseCase(repo)


def get_refresh_token_usecase(
    repo: AbstractUserRepository = Depends(get_user_repo)
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(repo)


def get_me_usecase(
    repo: AbstractUserRepository = Depends(get_user_repo),
) -> GetMeUseCase:
    return GetMeUseCase(repo)


# ── Auth Guard ──

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> int:
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return int(user_id)


# ── Flight Use Cases ──

def get_flight_detail_usecase(
    repo: AbstractFlightRepository = Depends(get_flight_repo)
) -> GetFlightDetailUseCase:
    return GetFlightDetailUseCase(repo)


# ── Booking Use Cases ──

def get_create_booking_usecase(
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
    flight_repo: AbstractFlightRepository = Depends(get_flight_repo),
    zone_repo: AbstractSeatZoneRepository = Depends(get_seat_zone_repo),
) -> CreateBookingUseCase:
    return CreateBookingUseCase(booking_repo, flight_repo, zone_repo)


def get_get_booking_usecase(
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
) -> GetBookingUseCase:
    return GetBookingUseCase(booking_repo)


def get_booking_detail_usecase(
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
    flight_repo: AbstractFlightRepository = Depends(get_flight_repo),
    passenger_repo: AbstractPassengerRepository = Depends(get_passenger_repo),
) -> GetBookingDetailUseCase:
    return GetBookingDetailUseCase(booking_repo, flight_repo, passenger_repo)


def get_calculate_price_usecase(
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
    flight_repo: AbstractFlightRepository = Depends(get_flight_repo),
    seat_repo: AbstractSeatRepository = Depends(get_seat_repo),
) -> CalculatePriceUseCase:
    return CalculatePriceUseCase(booking_repo, flight_repo, seat_repo)


def get_mock_payment_usecase(
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
) -> MockPaymentUseCase:
    return MockPaymentUseCase(booking_repo)


# ── Seat Use Cases ──

def get_seat_layout_usecase(
    repo: AbstractSeatRepository = Depends(get_seat_repo),
) -> GetSeatLayoutUseCase:
    return GetSeatLayoutUseCase(repo)


def get_select_seat_usecase(
    seat_repo: AbstractSeatRepository = Depends(get_seat_repo),
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
) -> SelectSeatUseCase:
    return SelectSeatUseCase(seat_repo, booking_repo)


def get_seat_zones_usecase(
    zone_repo: AbstractSeatZoneRepository = Depends(get_seat_zone_repo),
    seat_repo: AbstractSeatRepository = Depends(get_seat_repo),
) -> GetSeatZonesUseCase:
    return GetSeatZonesUseCase(zone_repo, seat_repo)


# ── Service Use Cases ──

def get_eligible_services_usecase(
    service_repo: AbstractServiceRepository = Depends(get_service_repo),
) -> GetEligibleServicesUseCase:
    return GetEligibleServicesUseCase(service_repo)


def get_service_limits_usecase() -> GetServiceLimitsUseCase:
    return GetServiceLimitsUseCase()


def get_assign_services_usecase(
    passenger_repo: AbstractPassengerRepository = Depends(get_passenger_repo),
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
    service_repo: AbstractServiceRepository = Depends(get_service_repo),
) -> AssignServicesUseCase:
    return AssignServicesUseCase(passenger_repo, booking_repo, service_repo)


# ── Passenger Use Cases ──

def get_create_passengers_usecase(
    passenger_repo: AbstractPassengerRepository = Depends(get_passenger_repo),
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
) -> CreatePassengersUseCase:
    return CreatePassengersUseCase(passenger_repo, booking_repo)


def get_update_passenger_usecase(
    passenger_repo: AbstractPassengerRepository = Depends(get_passenger_repo),
    booking_repo: AbstractBookingRepository = Depends(get_booking_repo),
) -> UpdatePassengerUseCase:
    return UpdatePassengerUseCase(passenger_repo, booking_repo)
