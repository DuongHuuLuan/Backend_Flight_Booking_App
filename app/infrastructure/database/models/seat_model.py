from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base


class SeatModel(Base):
    __tablename__ = "seats"
    id = Column(String(36), primary_key=True, index=True)
    flight_id = Column(String(36), ForeignKey("flights.id"), nullable=False)
    seat_label = Column(String(10), nullable=False)
    cabin_class = Column(String(20), nullable=False)
    row_number = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    zone_id = Column(String(36), ForeignKey("seat_zones.id"))

    zone = relationship("SeatZoneModel", back_populates="seats")
