from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.presentation.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: có thể init DB pool tại đây
    yield
    # Shutdown: cleanup


app = FastAPI(
    title="Flight Booking API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": None,
            "message": exc.message,
            "status": exc.status_code,
            "success": False,
        },
    )