from fastapi import APIRouter, Depends, Query
from app.shared.dependencies import get_countries_usecase, get_cities_usecase
from app.application.use_case.location.get_countries_usecase import GetCountriesUseCase
from app.application.use_case.location.get_cities_usecase import GetCitiesUseCase
from app.application.dto.common import BaseResponse
from app.application.dto.location_dto import CountriesResponse, CitiesResponse

router = APIRouter(prefix="/location", tags=["location"])


@router.get("/countries")
async def get_countries(
    uc: GetCountriesUseCase = Depends(get_countries_usecase),
):
    countries = await uc.execute()
    return BaseResponse(data=CountriesResponse(countries=countries), success=True)


@router.get("/cities")
async def get_cities(
    country: str = Query(alias="countryId"),
    uc: GetCitiesUseCase = Depends(get_cities_usecase),
):
    cities = await uc.execute(country)
    return BaseResponse(data=CitiesResponse(cities=cities), success=True)