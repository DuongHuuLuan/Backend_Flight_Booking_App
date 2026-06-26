from datetime import date, datetime
from pydantic import BaseModel


class PassengerData(BaseModel):
    name: str
    mobile_phone: str
    date_of_birth: date
    passport_number: str
    nationality: str
    seat_label: str | None = None
    age_group: str | None = None
    address: str | None = None
    email: str | None = None
    id_number: str | None = None


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
    seatLabel: str | None = None
    ageGroup: str | None = None
    address: str | None = None
    email: str | None = None
    idNumber: str | None = None
    baggageLevel: str = "none"


class UpdatePassengerRequest(BaseModel):
    name: str | None = None
    mobile_phone: str | None = None
    date_of_birth: date | None = None
    passport_number: str | None = None
    nationality: str | None = None
    address: str | None = None
    email: str | None = None
    id_number: str | None = None
    age_group: str | None = None
    seat_label: str | None = None
    baggage_level: str | None = None
