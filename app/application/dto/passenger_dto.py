from datetime import date, datetime
from pydantic import BaseModel


class PassengerData(BaseModel):
    name: str
    mobile_phone: str
    date_of_birth: date
    passport_number: str
    nationality: str


class CreatePassengersRequest(BaseModel):
    passengers: list[PassengerData]


class PassengerResponse(BaseModel):
    id: str
    bookingId: str
    name: str
    mobilePhone: str
    dateOfBirth: date
    passportNumber: str
    nationality: str
    createdAt: datetime
