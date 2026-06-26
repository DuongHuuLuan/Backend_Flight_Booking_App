from pydantic import BaseModel


class ServiceResponse(BaseModel):
    id: str
    type: str
    name: str
    description: str
    price: float
    maxPerPassenger: int


class ServiceLimitResponse(BaseModel):
    serviceType: str
    maxQuantity: int
    limitType: str


class EligibleServicesResponse(BaseModel):
    meals: list[ServiceResponse]
    drinks: list[ServiceResponse]
    baggage: list[ServiceResponse]
    limits: list[ServiceLimitResponse]


class PassengerServiceInput(BaseModel):
    passenger_id: str
    service_ids: list[str]
    baggage_level: str = "none"


class AssignServicesRequest(BaseModel):
    passengers: list[PassengerServiceInput]
