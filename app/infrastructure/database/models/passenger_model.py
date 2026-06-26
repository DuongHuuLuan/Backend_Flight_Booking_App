from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from app.infrastructure.database.base import Base


class PassengerModel(Base):
    __tablename__ = "passengers"

    id = Column(String(36), primary_key=True, index=True, nullable=False)
    booking_id = Column(String(36), ForeignKey("bookings.id"), nullable=False)
    name = Column(String(100), nullable=False)
    mobile_phone = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    passport_number = Column(String(50), nullable=False)
    nationality = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    seat_label = Column(String(10))
    age_group = Column(String(10))
    address = Column(String(255))
    email = Column(String(100))
    id_number = Column(String(50))
    baggage_level = Column(String(20), default="none")
