from dataclasses import dataclass


@dataclass
class ServiceEntity:
    id: str
    type: str
    name: str
    description: str
    price: float
    max_per_passenger: int
    is_active: bool
