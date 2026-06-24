from app.domain.entities.passenger_entity import PassengerEntity
from app.infrastructure.database.models.passenger_model import PassengerModel


class PassengerMapper:
    @staticmethod
    def to_entity(model: PassengerModel) -> PassengerEntity:
        return PassengerEntity(
            id=model.id,
            booking_id=model.booking_id,
            name=model.name,
            mobile_phone=model.mobile_phone,
            date_of_birth=model.date_of_birth,
            passport_number=model.passport_number,
            nationality=model.nationality,
            created_at=model.created_at,
        )
