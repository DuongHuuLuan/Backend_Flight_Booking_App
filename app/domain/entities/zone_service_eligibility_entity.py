from dataclasses import dataclass


@dataclass
class ZoneServiceEligibilityEntity:
    id: str
    zone_id: str
    service_id: str
    age_group: str
