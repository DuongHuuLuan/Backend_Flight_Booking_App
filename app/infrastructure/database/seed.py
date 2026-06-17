import asyncio
from datetime import datetime
from sqlalchemy import select
from app.infrastructure.database.session import async_session_factory
from app.infrastructure.database.models.country_model import CountryModel
from app.infrastructure.database.models.city_model import CityModel
from app.infrastructure.database.models.airline_model import AirlineModel
from app.infrastructure.database.models.airport_model import AirportModel
from app.infrastructure.database.models.flight_model import FlightModel


async def seed():
    async with async_session_factory() as db:
        # Kiểm tra đã seed chưa
        result = await db.execute(select(CountryModel).limit(1))
        if result.scalar_one_or_none():
            print("Data already seeded, skipping...")
            return

        # ── Countries ──
        countries_data = ["Vietnam", "United States", "Japan", "China", "UAE", "New Zealand"]
        countries = [CountryModel(name=n) for n in countries_data]
        db.add_all(countries)
        await db.flush()

        # ── Cities ──
        cities_data = [
            ("Ho Chi Minh", "Vietnam"), ("Hanoi", "Vietnam"), ("Da Nang", "Vietnam"),
            ("New York", "United States"), ("Los Angeles", "United States"), ("Chicago", "United States"),
            ("Tokyo", "Japan"), ("Osaka", "Japan"), ("Kyoto", "Japan"),
            ("Beijing", "China"), ("Shanghai", "China"), ("Guangzhou", "China"),
            ("Dubai", "UAE"), ("Auckland", "New Zealand"),
        ]
        country_map = {c.name: c.id for c in countries}
        cities = [CityModel(name=name, country_id=country_map[country]) for name, country in cities_data]
        db.add_all(cities)

        # ── Airlines ──
        airlines_data = [
            ("VN", "Vietnam Airlines", ""),
            ("VJ", "VietJet Air", ""),
            ("QH", "Bamboo Airways", ""),
            ("QR", "Qatar Airways", ""),
            ("EK", "Emirates", ""),
            ("SQ", "Singapore Airlines", ""),
            ("QF", "Qantas", ""),
        ]
        airlines = [AirlineModel(id=i, name=n, logo_url=l) for i, n, l in airlines_data]
        db.add_all(airlines)
        await db.flush()

        # ── Airports ──
        airports_data = [
            ("SGN", "Tan Son Nhat", "Ho Chi Minh", "Vietnam"),
            ("HAN", "Noi Bai", "Hanoi", "Vietnam"),
            ("DAD", "Da Nang", "Da Nang", "Vietnam"),
            ("DXB", "Dubai International Airport", "Dubai", "UAE"),
            ("AKL", "Auckland Airport", "Auckland", "New Zealand"),
        ]
        airports = [
            AirportModel(code=c, name=n, city=ct, country=co)
            for c, n, ct, co in airports_data
        ]
        db.add_all(airports)
        await db.flush()

        # ── Flights (chính xác 13 records từ mock Flutter) ──
        flights = [
            FlightModel(id="FL001", airline_id="VN", flight_number="VN123",
                departure_airport_code="SGN", arrival_airport_code="HAN",
                departure_time=datetime(2026, 6, 1, 8, 0), arrival_time=datetime(2026, 6, 1, 10, 0),
                duration_minutes=120, price=1500000, stops=0, cabin_class="economy"),

            FlightModel(id="FL002", airline_id="VJ", flight_number="VJ456",
                departure_airport_code="SGN", arrival_airport_code="DAD",
                departure_time=datetime(2026, 6, 1, 14, 30), arrival_time=datetime(2026, 6, 1, 15, 45),
                duration_minutes=75, price=800000, stops=0, cabin_class="economy"),

            FlightModel(id="FL003", airline_id="QH", flight_number="QH789",
                departure_airport_code="HAN", arrival_airport_code="SGN",
                departure_time=datetime(2026, 6, 2, 6, 0), arrival_time=datetime(2026, 6, 2, 8, 15),
                duration_minutes=135, price=1200000, stops=0, cabin_class="business"),

            FlightModel(id="FL004", airline_id="VN", flight_number="VN888",
                departure_airport_code="SGN", arrival_airport_code="HAN",
                departure_time=datetime(2026, 6, 1, 19, 0), arrival_time=datetime(2026, 6, 1, 21, 0),
                duration_minutes=120, price=2500000, stops=0, cabin_class="business"),

            FlightModel(id="FL005", airline_id="VJ", flight_number="VJ222",
                departure_airport_code="DAD", arrival_airport_code="SGN",
                departure_time=datetime(2026, 6, 3, 9, 30), arrival_time=datetime(2026, 6, 3, 10, 45),
                duration_minutes=75, price=700000, stops=0, cabin_class="economy"),

            FlightModel(id="FL006", airline_id="VN", flight_number="VN666",
                departure_airport_code="SGN", arrival_airport_code="HAN",
                departure_time=datetime(2026, 6, 2, 6, 30), arrival_time=datetime(2026, 6, 2, 8, 30),
                duration_minutes=120, price=5000000, stops=0, cabin_class="first"),

            FlightModel(id="FL007", airline_id="QH", flight_number="QH111",
                departure_airport_code="HAN", arrival_airport_code="DAD",
                departure_time=datetime(2026, 6, 4, 14, 0), arrival_time=datetime(2026, 6, 4, 15, 15),
                duration_minutes=75, price=1800000, stops=0, cabin_class="economy"),

            FlightModel(id="FL008", airline_id="QR", flight_number="QR920",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 17, 45), arrival_time=datetime(2026, 6, 6, 13, 5),
                duration_minutes=1340, price=1400, stops=1, cabin_class="economy"),

            FlightModel(id="FL009", airline_id="EK", flight_number="EK448",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 10, 45), arrival_time=datetime(2026, 6, 6, 18, 55),
                duration_minutes=1390, price=1530, stops=1, cabin_class="economy"),

            FlightModel(id="FL010", airline_id="SQ", flight_number="SQ285",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 23, 0), arrival_time=datetime(2026, 6, 6, 19, 20),
                duration_minutes=1340, price=1210, stops=1, cabin_class="economy"),

            FlightModel(id="FL011", airline_id="QF", flight_number="QF842",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 23, 15), arrival_time=datetime(2026, 6, 6, 18, 55),
                duration_minutes=1270, price=1160, stops=1, cabin_class="economy"),

            FlightModel(id="FL012", airline_id="EK", flight_number="EK451",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 6, 0), arrival_time=datetime(2026, 6, 5, 21, 30),
                duration_minutes=930, price=1890, stops=0, cabin_class="first"),

            FlightModel(id="FL013", airline_id="QR", flight_number="QR923",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 19, 45), arrival_time=datetime(2026, 6, 6, 11, 0),
                duration_minutes=915, price=980, stops=2, cabin_class="economy"),
        ]
        db.add_all(flights)
        await db.commit()
        print(f"Seed complete: {len(countries)} countries, {len(cities)} cities, "
              f"{len(airlines)} airlines, {len(airports)} airports, {len(flights)} flights")


if __name__ == "__main__":
    asyncio.run(seed())