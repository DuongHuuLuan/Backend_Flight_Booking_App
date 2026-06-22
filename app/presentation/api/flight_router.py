from fastapi import APIRouter, Depends, HTTPException, Query
from app.application.use_case.flight.get_flight_detail_usecase import GetFlightDetailUseCase
from app.shared.dependencies import (
    get_popular_flights_usecase, get_search_flights_usecase,
    get_all_flights_usecase, get_flight_detail_usecase,
)
from app.application.use_case.flight.get_popular_flights_usecase import GetPopularFlightsUseCase
from app.application.use_case.flight.search_flights_usecase import SearchFlightsUseCase
from app.application.use_case.flight.get_all_flights_usecase import GetAllFlightsUseCase
from app.application.dto.common import BaseResponse
from app.application.dto.flight_dto import FlightDetailResponse, FlightSearchRequest, FlightResponse, AirportResponse, AirlineResponse

router = APIRouter(tags=["flights"])


def _to_flight_response(flight) -> FlightResponse:
    return FlightResponse(
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
        price=flight.price,
        stops=flight.stops,
        cabinClass=flight.cabin_class,
    )


@router.get("/home/popular")
async def get_popular(
    uc: GetPopularFlightsUseCase = Depends(get_popular_flights_usecase),
):
    flights = await uc.execute()
    return BaseResponse(data=[_to_flight_response(f) for f in flights], success=True)


@router.post("/home/search")
async def search_flights(
    body: FlightSearchRequest,
    uc: SearchFlightsUseCase = Depends(get_search_flights_usecase),
):
    from app.domain.entities.flight_search_params import FlightSearchParams
    from datetime import date
    params = FlightSearchParams(
        trip_type=body.trip_type,
        origin=body.origin,
        destination=body.destination,
        departure_date=date.fromisoformat(body.departure_date),
        return_date=date.fromisoformat(body.return_date) if body.return_date else None,
        passengers=body.passengers,
        cabin_class=body.cabin_class,
    )
    flights = await uc.execute(params)
    return BaseResponse(data=[_to_flight_response(f) for f in flights], success=True)


@router.get("/flights")
async def get_all_flights(
    uc: GetAllFlightsUseCase = Depends(get_all_flights_usecase),
):
    flights = await uc.execute()
    return BaseResponse(data=[_to_flight_response(f) for f in flights], success=True)

@router.get("/flights/{flight_id}", response_model=BaseResponse[FlightDetailResponse])
async def get_flight_detail(
    flight_id: str,
    uc: GetFlightDetailUseCase = Depends(get_flight_detail_usecase)
):
    result = await uc.execute(flight_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return BaseResponse(data=result, success=True)