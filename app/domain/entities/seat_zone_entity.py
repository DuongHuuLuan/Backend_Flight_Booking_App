from dataclasses import dataclass


@dataclass
class SeatZoneEntity:
    id: str
    name: str
    price_modifier: float
    description: str
    color_hex: str
