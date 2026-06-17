from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base

class AirlineModel(Base):
    __tablename__ = "airlines"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    logo_url = Column(String(255))

    flights = relationship(
        "FlightModel",
        back_populates="airline"
    )