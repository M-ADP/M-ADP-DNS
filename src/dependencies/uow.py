from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_session
from src.core.uow import UnitOfWork


def get_uow(session: AsyncSession = Depends(get_session)) -> UnitOfWork:
    return UnitOfWork(session)
