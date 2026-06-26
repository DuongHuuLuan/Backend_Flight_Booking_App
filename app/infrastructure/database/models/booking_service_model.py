from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.infrastructure.database.base import Base


class BookingServiceModel(Base):
    __tablename__ = "booking_services"

    id = Column(String(36), primary_key=True)
    booking_id = Column(String(36), ForeignKey("bookings.id"), nullable=False)
    passenger_id = Column(String(36), ForeignKey("passengers.id"), nullable=False)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
