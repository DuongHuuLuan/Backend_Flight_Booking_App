from fastapi import APIRouter
from .auth_router import router as auth_router
from .flight_router import router as flight_router
from .location_router import router as location_router
from .health_router import router as health_router
from .booking_router import router as booking_router
api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(flight_router)
api_router.include_router(location_router)
api_router.include_router(health_router)
api_router.include_router(booking_router)