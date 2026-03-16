from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    message: str
    data: T


class CursorPage(BaseModel, Generic[T]):
    cursor: int | None
    items: List[T]


class ErrorResponse(BaseModel):
    message: str
