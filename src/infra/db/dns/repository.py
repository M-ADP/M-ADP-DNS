from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.dns import DNS
from src.core.repository.dns_repository import DNSRepository
from src.infra.db.dns.model import DNS as DNSModel


class DNSRepositoryImpl(DNSRepository):
    """DNS Repository 구현체"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def insert(self, dns: DNS) -> DNS:
        model = DNSModel(
            id=dns.id,
            project_id=dns.project_id,
            deployment_id=dns.deployment_id,
            subdomain=dns.subdomain,
        )
        self._session.add(model)
        await self._session.flush()
        return model.to_entity()

    async def get_by_id(self, dns_id: int) -> DNS | None:
        stmt = select(DNSModel).where(DNSModel.id == dns_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None

    async def list_by_project(
        self,
        project_id: int,
        limit: int,
        cursor: int | None = None,
    ) -> List[DNS]:
        conditions = [DNSModel.project_id == project_id]
        if cursor:
            conditions.append(DNSModel.id < cursor)

        stmt = (
            select(DNSModel)
            .where(*conditions)
            .order_by(DNSModel.id.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [model.to_entity() for model in result.scalars().all()]

    async def delete(self, dns: DNS) -> None:
        model = await self._session.get(DNSModel, dns.id)
        if model is None:
            return
        await self._session.delete(model)
        await self._session.flush()

    async def update_subdomain(self, dns_id: int, subdomain: str) -> DNS:
        stmt = select(DNSModel).where(DNSModel.id == dns_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            raise ValueError(f"DNS not found: {dns_id}")
        model.subdomain = subdomain
        await self._session.flush()
        return model.to_entity()

    async def exists_by_subdomain(
        self,
        subdomain: str,
        exclude_dns_id: int | None = None,
    ) -> bool:
        conditions = [DNSModel.subdomain == subdomain]
        if exclude_dns_id is not None:
            conditions.append(DNSModel.id != exclude_dns_id)
        stmt = select(DNSModel.id).where(*conditions).limit(1)
        result = await self._session.execute(stmt)
        return result.first() is not None
