from dataclasses import dataclass

@dataclass
class AirportEntity:
    code: str
    name: str
    city: str
    country: str