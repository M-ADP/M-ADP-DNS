from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class Repository(Generic[T], ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
