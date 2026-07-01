import asyncio
from datetime import datetime
from sqlalchemy import select
from app.infrastructure.database.models.seat_model import SeatModel
from app.infrastructure.database.session import async_session_factory
from app.infrastructure.database.models.country_model import CountryModel
from app.infrastructure.database.models.city_model import CityModel
from app.infrastructure.database.models.airline_model import AirlineModel
from app.infrastructure.database.models.airport_model import AirportModel
from app.infrastructure.database.models.flight_model import FlightModel
from app.infrastructure.database.models.seat_zone_model import SeatZoneModel
from app.infrastructure.database.models.service_model import ServiceModel
from app.infrastructure.database.models.zone_service_eligibility_model import (
    ZoneServiceEligibilityModel,
)
from app.infrastructure.database.models.booking_model import BookingModel
from app.infrastructure.database.models.passenger_model import PassengerModel
from app.infrastructure.database.models.booking_service_model import BookingServiceModel


async def seed():
    async with async_session_factory() as db:
        # Kiểm tra đã seed chưa (dùng SeatZoneModel thay vì CountryModel)
        result = await db.execute(select(SeatZoneModel).limit(1))
        if result.scalar_one_or_none():
            print("Data already seeded, skipping...")
            return

        # Xoá dữ liệu cũ nếu có (tránh duplicate key) — thứ tự con→cha
        for table in [BookingServiceModel, ZoneServiceEligibilityModel,
                      PassengerModel, BookingModel,
                      SeatModel, ServiceModel, SeatZoneModel,
                      FlightModel, AirportModel, AirlineModel,
                      CityModel, CountryModel]:
            await db.execute(table.__table__.delete())
        await db.commit()

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

        # ── Seat Zones ──
        zones = [
            SeatZoneModel(id="ZONE_VIP",  name="VIP",    price_modifier=2.0, description="Khu vực VIP cao cấp, hàng ghế 1-6",   color_hex="#FFD700"),
            SeatZoneModel(id="ZONE_MID",  name="Trung",  price_modifier=1.0, description="Khu vực trung tâm, hàng ghế 7-13",  color_hex="#4CAF50"),
            SeatZoneModel(id="ZONE_STD",  name="Thường", price_modifier=0.7, description="Khu vực tiêu chuẩn, hàng ghế 14-20", color_hex="#9E9E9E"),
        ]
        db.add_all(zones)
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
                duration_minutes=120, price=1500000, stops=0),

            FlightModel(id="FL002", airline_id="VJ", flight_number="VJ456",
                departure_airport_code="SGN", arrival_airport_code="DAD",
                departure_time=datetime(2026, 6, 1, 14, 30), arrival_time=datetime(2026, 6, 1, 15, 45),
                duration_minutes=75, price=800000, stops=0),

            FlightModel(id="FL003", airline_id="QH", flight_number="QH789",
                departure_airport_code="HAN", arrival_airport_code="SGN",
                departure_time=datetime(2026, 6, 2, 6, 0), arrival_time=datetime(2026, 6, 2, 8, 15),
                duration_minutes=135, price=1200000, stops=0),

            FlightModel(id="FL004", airline_id="VN", flight_number="VN888",
                departure_airport_code="SGN", arrival_airport_code="HAN",
                departure_time=datetime(2026, 6, 1, 19, 0), arrival_time=datetime(2026, 6, 1, 21, 0),
                duration_minutes=120, price=2500000, stops=0),

            FlightModel(id="FL005", airline_id="VJ", flight_number="VJ222",
                departure_airport_code="DAD", arrival_airport_code="SGN",
                departure_time=datetime(2026, 6, 3, 9, 30), arrival_time=datetime(2026, 6, 3, 10, 45),
                duration_minutes=75, price=700000, stops=0),

            FlightModel(id="FL006", airline_id="VN", flight_number="VN666",
                departure_airport_code="SGN", arrival_airport_code="HAN",
                departure_time=datetime(2026, 6, 2, 6, 30), arrival_time=datetime(2026, 6, 2, 8, 30),
                duration_minutes=120, price=5000000, stops=0),

            FlightModel(id="FL007", airline_id="QH", flight_number="QH111",
                departure_airport_code="HAN", arrival_airport_code="DAD",
                departure_time=datetime(2026, 6, 4, 14, 0), arrival_time=datetime(2026, 6, 4, 15, 15),
                duration_minutes=75, price=1800000, stops=0),

            FlightModel(id="FL008", airline_id="QR", flight_number="QR920",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 17, 45), arrival_time=datetime(2026, 6, 6, 13, 5),
                duration_minutes=1340, price=1400, stops=1),

            FlightModel(id="FL009", airline_id="EK", flight_number="EK448",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 10, 45), arrival_time=datetime(2026, 6, 6, 18, 55),
                duration_minutes=1390, price=1530, stops=1),

            FlightModel(id="FL010", airline_id="SQ", flight_number="SQ285",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 23, 0), arrival_time=datetime(2026, 6, 6, 19, 20),
                duration_minutes=1340, price=1210, stops=1),

            FlightModel(id="FL011", airline_id="QF", flight_number="QF842",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 23, 15), arrival_time=datetime(2026, 6, 6, 18, 55),
                duration_minutes=1270, price=1160, stops=1),

            FlightModel(id="FL012", airline_id="EK", flight_number="EK451",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 6, 0), arrival_time=datetime(2026, 6, 5, 21, 30),
                duration_minutes=930, price=1890, stops=0),

            FlightModel(id="FL013", airline_id="QR", flight_number="QR923",
                departure_airport_code="DXB", arrival_airport_code="AKL",
                departure_time=datetime(2026, 6, 5, 19, 45), arrival_time=datetime(2026, 6, 6, 11, 0),
                duration_minutes=915, price=980, stops=2),
        ]
        db.add_all(flights)
        await db.flush()

        # ── Zone map for seats ──
        zone_map = {}
        for row in range(1, 21):
            if row <= 6:
                zone_map[row] = "ZONE_VIP"
            elif row <= 13:
                zone_map[row] = "ZONE_MID"
            else:
                zone_map[row] = "ZONE_STD"

        seat_labels = []
        for row in range(1, 21):
            for pos, label in enumerate(["A", "B", "C", "D"], start=1):
                seat_labels.append((f"{row}{label}", row, pos))

        for flight in flights:
            for label, row, pos in seat_labels:
                db.add(SeatModel(
                    id=f"{flight.id}-{label}",
                    flight_id=flight.id,
                    seat_label=label,
                    row_number=row,
                    position=pos,
                    is_available=True,
                    zone_id=zone_map[row],
                ))
        await db.flush()

        # ── Services ──
        services = [
            ServiceModel(id="SVC_MEAL_VIP",   type="meal",    name="Suất VIP hảo hạng",   price=200000, max_per_passenger=1),
            ServiceModel(id="SVC_MEAL_MID",   type="meal",    name="Suất ăn thương gia",  price=100000, max_per_passenger=1),
            ServiceModel(id="SVC_MEAL_STD",   type="meal",    name="Suất ăn cơ bản",      price=50000,  max_per_passenger=1),
            ServiceModel(id="SVC_MEAL_CHILD", type="meal",    name="Suất ăn trẻ em",      price=30000,  max_per_passenger=1),
            ServiceModel(id="SVC_MEAL_DIET",  type="meal",    name="Suất ăn kiêng",       price=80000,  max_per_passenger=1),
            ServiceModel(id="SVC_DRINK_VIP",  type="drink",   name="Đồ uống cao cấp",     price=100000, max_per_passenger=2),
            ServiceModel(id="SVC_DRINK_MID",  type="drink",   name="Đồ uống thường",      price=30000,  max_per_passenger=2),
            ServiceModel(id="SVC_DRINK_CHILD",type="drink",   name="Đồ uống trẻ em",      price=20000,  max_per_passenger=2),
            ServiceModel(id="SVC_BAG_1",     type="baggage", name="Hành lý 20kg",         price=200000, max_per_passenger=1),
            ServiceModel(id="SVC_BAG_2",     type="baggage", name="Hành lý 30kg",         price=350000, max_per_passenger=1),
            ServiceModel(id="SVC_BAG_3",     type="baggage", name="Hành lý 40kg",         price=500000, max_per_passenger=1),
        ]
        db.add_all(services)
        await db.flush()

        # ── Zone Service Eligibility ──
        meal_drink_rules = [
            ("ZONE_VIP", "SVC_MEAL_VIP",   "child"),  ("ZONE_VIP", "SVC_MEAL_VIP",   "adult"),
            ("ZONE_VIP", "SVC_MEAL_VIP",   "senior"),
            ("ZONE_VIP", "SVC_MEAL_CHILD", "child"),  ("ZONE_VIP", "SVC_DRINK_CHILD","child"),
            ("ZONE_VIP", "SVC_DRINK_VIP",  "adult"),  ("ZONE_VIP", "SVC_DRINK_VIP",  "senior"),
            ("ZONE_MID", "SVC_MEAL_MID",   "adult"),  ("ZONE_MID", "SVC_MEAL_DIET",  "senior"),
            ("ZONE_MID", "SVC_MEAL_CHILD", "child"),  ("ZONE_MID", "SVC_DRINK_MID",  "adult"),
            ("ZONE_MID", "SVC_DRINK_MID",  "senior"), ("ZONE_MID", "SVC_DRINK_CHILD","child"),
            ("ZONE_STD", "SVC_MEAL_STD",   "adult"),  ("ZONE_STD", "SVC_MEAL_DIET",  "senior"),
            ("ZONE_STD", "SVC_MEAL_CHILD", "child"),  ("ZONE_STD", "SVC_DRINK_MID",  "adult"),
            ("ZONE_STD", "SVC_DRINK_MID",  "senior"), ("ZONE_STD", "SVC_DRINK_CHILD","child"),
        ]

        baggage_rules = []
        for zone_id in ["ZONE_VIP", "ZONE_MID", "ZONE_STD"]:
            for age in ["child", "adult", "senior"]:
                for bag_id in ["SVC_BAG_1", "SVC_BAG_2", "SVC_BAG_3"]:
                    baggage_rules.append((zone_id, bag_id, age))

        all_rules = meal_drink_rules + baggage_rules
        db.add_all([
            ZoneServiceEligibilityModel(id=f"ELIG_{i}", zone_id=z, service_id=s, age_group=a)
            for i, (z, s, a) in enumerate(all_rules)
        ])

        await db.commit()
        print(f"Seed complete: {len(countries)} countries, {len(cities)} cities, "
              f"{len(airlines)} airlines, {len(zones)} zones, {len(airports)} airports, "
              f"{len(flights)} flights, {len(services)} services, {len(all_rules)} eligibility rules")


if __name__ == "__main__":
    asyncio.run(seed())