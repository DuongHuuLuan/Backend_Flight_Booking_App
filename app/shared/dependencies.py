from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.infrastructure.database.session import get_db as _get_db
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException

from app.domain.repositories.user_repository import AbstractUserRepository
from app.domain.repositories.flight_repository import AbstractFlightRepository
from app.domain.repositories.location_repository import AbstractLocationRepository

from app.infrastructure.repositories.user_repository_impl import UserRepository
from app.infrastructure.repositories.flight_repository_impl import FlightRepository
from app.infrastructure.repositories.location_repository_impl import LocationRepository
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

#-- Auth use case
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