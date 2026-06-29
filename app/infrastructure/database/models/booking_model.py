from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(String(36), primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flight_id = Column(String(36), ForeignKey("flights.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), default="confirmed")
    selected_seat = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    zone_price_total = Column(Float, default=0)
    service_total = Column(Float, default=0)
    baggage_total = Column(Float, default=0)

    user = relationship("UserModel", back_populates="bookings")
    flight = relationship("FlightModel", back_populates="bookings")