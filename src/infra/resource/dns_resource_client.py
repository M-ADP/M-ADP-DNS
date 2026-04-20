from typing import List

import aiohttp

from src.core.client.dns_resource import DNSResourceClient
from src.core.domain.dns import DNS
from src.infra.resource.exceptions import ResourceNotFoundException, ResourceServerException


class DNSResourceClientImpl(DNSResourceClient):
    """DNS 리소스 서버 HTTP 클라이언트 구현체"""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    async def _request(self, coro) -> None:
        try:
            response = await coro
        except Exception as e:
            raise ResourceServerException() from e
        if response.status == 404:
            raise ResourceNotFoundException()
        if not response.ok:
            raise ResourceServerException(
                f"리소스 서버 응답 오류: {response.status}"
            )

    async def create(self, dns: DNS) -> None:
        async with aiohttp.ClientSession(base_url=self._base_url) as session:
            await self._request(
                session.post(
                    "/apps/dns",
                    json={
                        "id": str(dns.id),
                        "project_id": str(dns.project_id),
                        "deployment_id": str(dns.deployment_id),
                        "subdomain": dns.subdomain,
                    },
                )
            )

    async def delete(self, dns: DNS) -> None:
        async with aiohttp.ClientSession(base_url=self._base_url) as session:
            await self._request(session.delete(f"/apps/dns/{dns.id}"))

    async def update(self, dns: DNS) -> None:
        async with aiohttp.ClientSession(base_url=self._base_url) as session:
            await self._request(
                session.put(
                    f"/apps/dns/{dns.id}",
                    json={
                        "project_id": str(dns.project_id),
                        "deployment_id": str(dns.deployment_id),
                        "subdomain": dns.subdomain,
                        "service_type": dns.service_type,
                    },
                )
            )

    async def list_by_project(self, project_id: int) -> List[DNS]:
        raise NotImplementedError
