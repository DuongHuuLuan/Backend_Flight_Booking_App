from app.domain.entities.seat_entity import SeatEntity
from app.infrastructure.database.models.seat_model import SeatModel


class SeatMapper:
    @staticmethod
    def to_entity(model: SeatModel) -> SeatEntity:
        return SeatEntity(
            id=model.id,
            flight_id=model.flight_id,
            seat_label=model.seat_label,
            cabin_class=model.cabin_class,
            row_number=model.row_number,
            position=model.position,
            is_available=model.is_available
        )
            