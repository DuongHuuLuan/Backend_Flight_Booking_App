from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class PassengerEntity:
    id: str
    booking_id: str
    name: str
    mobile_phone: str
    date_of_birth: date
    passport_number: str
    nationality: str
    created_at: datetime
