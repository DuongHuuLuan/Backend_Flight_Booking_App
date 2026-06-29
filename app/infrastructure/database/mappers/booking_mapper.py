from app.domain.entities.booking_entity import BookingEntity
from app.infrastructure.database.models.booking_model import BookingModel


class BookingMapper:
    @staticmethod
    def to_entity(model: BookingModel) -> BookingEntity:
        return BookingEntity(
            id=model.id,
            user_id=model.user_id,
            flight_id=model.flight_id,
            total_price=model.total_price,
            status=model.status,
            selected_seat=model.selected_seat,
            created_at=model.created_at,
            zone_price_total=model.zone_price_total or 0,
            service_total=model.service_total or 0,
            baggage_total=model.baggage_total or 0,
        )
