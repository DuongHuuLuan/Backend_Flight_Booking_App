from pydantic import BaseModel
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    data: T | None = None
    message: str | None = None
    status: int | None = None
    success: bool | None = None