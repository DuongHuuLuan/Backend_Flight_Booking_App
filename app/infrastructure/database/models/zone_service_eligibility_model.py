from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class ZoneServiceEligibilityModel(Base):
    __tablename__ = "zone_service_eligibility"
    __table_args__ = (
        UniqueConstraint("zone_id", "service_id", "age_group", name="uq_zone_service_age"),
    )

    id = Column(String(36), primary_key=True)
    zone_id = Column(String(36), ForeignKey("seat_zones.id"), nullable=False)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    age_group = Column(String(10), nullable=False)

    zone = relationship("SeatZoneModel")
    service = relationship("ServiceModel", back_populates="eligibility_rules")
