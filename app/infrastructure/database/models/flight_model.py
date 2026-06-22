from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class FlightModel(Base):
    __tablename__ = "flights"

    id = Column(String(36), primary_key=True)
    airline_id = Column(
        String(36),
        ForeignKey("airlines.id")
    )
    departure_airport_code = Column(
        String(20),
        ForeignKey("airports.code")
    )
    arrival_airport_code = Column(
        String(20),
        ForeignKey("airports.code")
    )
    flight_number = Column(String(10))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    duration_minutes = Column(Integer)
    price = Column(Float)
    stops = Column(Integer)
    cabin_class = Column(String(20))


    airline = relationship(
        "AirlineModel",
        back_populates="flights"
    )
    departure_airport = relationship(
        "AirportModel",
        foreign_keys=[departure_airport_code]
    )
    arrival_airport = relationship(
        "AirportModel",
        foreign_keys=[arrival_airport_code],
        back_populates="arriving_flights"
    )
    
    bookings = relationship("BookingModel", back_populates="flight")