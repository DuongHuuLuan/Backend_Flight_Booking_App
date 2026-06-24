from app.domain.repositories.seat_repository import AbstractSeatRepository


class GetSeatLayoutUseCase:
    def __init__(self, seat_repo: AbstractSeatRepository):
        self.seat_repo = seat_repo

    async def execute(self, flight_id: str) -> list:
        return await self.seat_repo.get_by_flight(flight_id)