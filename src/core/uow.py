from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository.dns_repository import DNSRepository
from src.infra.db.dns.repository import DNSRepositoryImpl


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.dns: DNSRepository = DNSRepositoryImpl(session)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
