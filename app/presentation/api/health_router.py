from fastapi import APIRouter
from app.application.dto.common import BaseResponse

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return BaseResponse(data={"status": "ok"}, message="Server is running", success=True)