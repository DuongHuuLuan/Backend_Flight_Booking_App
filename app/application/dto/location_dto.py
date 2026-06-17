from pydantic import BaseModel


class CountriesResponse(BaseModel):
    countries: list[str]

class CitiesResponse(BaseModel):
    cities: list[str]