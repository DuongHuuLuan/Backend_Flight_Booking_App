from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class SeatZoneModel(Base):
    __tablename__ = "seat_zones"

    id = Column(String(36), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    price_modifier = Column(Float, nullable=False)
    description = Column(String(255))
    color_hex = Column(String(7))

    seats = relationship("SeatModel", back_populates="zone")
