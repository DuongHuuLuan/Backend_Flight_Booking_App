from app.domain.entities.booking_entity import BookingEntity
from app.infrastructure.database.models.booking_model import BookingModel


class BookingMapper:
    @staticmethod
    def to_entity(model: BookingModel) -> BookingEntity:
        return BookingEntity(
            id=model.id,
            user_id=model.user_id,
            flight_id=model.flight_id,
            cabin_class=model.cabin_class,
            total_price=model.total_price,
            status=model.status,
            selected_seat=model.selected_seat,
            created_at=model.created_at
        )