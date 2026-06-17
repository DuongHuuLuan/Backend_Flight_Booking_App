from app.domain.entities.user_entity import UserEntity
from app.infrastructure.database.models.user_model import UserModel


class UserMapper:

    @staticmethod
    def to_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id, name=model.name, email=model.email,
            phone=model.phone, country=model.country, city=model.city,
            password=model.password, avatar=model.avatar,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id, name=entity.name, email=entity.email,
            phone=entity.phone, country=entity.country, city=entity.city,
            password=entity.password, avatar=entity.avatar,
            created_at=entity.created_at,
        )

    @staticmethod
    def update_model(model: UserModel, entity: UserEntity) -> UserModel:
        model.name = entity.name
        model.email = entity.email
        model.phone = entity.phone
        model.country = entity.country
        model.city = entity.city
        model.password = entity.password
        model.avatar = entity.avatar
        return model