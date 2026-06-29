from app.domain.entities.airline_entity import AirlineEntity
from app.domain.entities.airport_entity import AirportEntity
from app.domain.entities.flight_entity import FlightEntity
from app.infrastructure.database.models.flight_model import FlightModel


class FlightMapper:

    @staticmethod
    def to_entity(model: FlightModel) -> FlightEntity:
        return FlightEntity(
            id=model.id,
            airline=AirlineEntity(
                id=model.airline.id,
                name=model.airline.name,
                logo_url=model.airline.logo_url,
            ),
            flight_number=model.flight_number,
            departure_airport=AirportEntity(
                code=model.departure_airport.code,
                name=model.departure_airport.name,
                city=model.departure_airport.city,
                country=model.departure_airport.country,
            ),
            arrival_airport=AirportEntity(
                code=model.arrival_airport.code,
                name=model.arrival_airport.name,
                city=model.arrival_airport.city,
                country=model.arrival_airport.country,
            ),
            departure_time=model.departure_time,
            arrival_time=model.arrival_time,
            duration_minutes=model.duration_minutes,
            price=model.price,
            stops=model.stops,
        )