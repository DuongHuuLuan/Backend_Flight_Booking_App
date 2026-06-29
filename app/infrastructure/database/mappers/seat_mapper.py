from app.domain.entities.seat_entity import SeatEntity
from app.domain.entities.seat_zone_entity import SeatZoneEntity
from app.infrastructure.database.models.seat_model import SeatModel


class SeatMapper:
    @staticmethod
    def to_entity(model: SeatModel) -> SeatEntity:
        zone = None
        if model.zone:
            zone = SeatZoneEntity(
                id=model.zone.id,
                name=model.zone.name,
                price_modifier=model.zone.price_modifier,
                description=model.zone.description or "",
                color_hex=model.zone.color_hex or "",
            )
        return SeatEntity(
            id=model.id,
            flight_id=model.flight_id,
            seat_label=model.seat_label,
            cabin_class=model.cabin_class,
            row_number=model.row_number,
            position=model.position,
            is_available=model.is_available,
            zone=zone,
        )
