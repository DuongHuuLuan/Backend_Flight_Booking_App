
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class AirportModel(Base):
    __tablename__ = "airports"
    code = Column(String(20), primary_key=True)
    name = Column(String(255), nullable=False)
    city = Column(String(255))
    country = Column(String(255))
    
    departing_flights = relationship(
        "FlightModel",
        foreign_keys="FlightModel.departure_airport_code",
        back_populates="departure_airport"
    )

    arriving_flights = relationship(
        "FlightModel",
        foreign_keys="FlightModel.arrival_airport_code",
        back_populates="arrival_airport"
    )