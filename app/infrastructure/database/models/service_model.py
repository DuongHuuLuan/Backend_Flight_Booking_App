from sqlalchemy import Column, String, Text, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class ServiceModel(Base):
    __tablename__ = "services"

    id = Column(String(36), primary_key=True)
    type = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    max_per_passenger = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    eligibility_rules = relationship("ZoneServiceEligibilityModel", back_populates="service")
