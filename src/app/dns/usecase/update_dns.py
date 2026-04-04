from fastapi import Depends

from src.app.base_usecase import BaseUseCase
from src.app.dns.exceptions import DNSAlreadyExists, DNSNotFound, ResourceServerError
from src.app.dns.schemas import DNSUpdate
from src.core.client.dns_resource import DNSResourceClient
from src.core.domain.dns import DNS
from src.core.uow import UnitOfWork
from src.dependencies.resource_client import get_resource_client
from src.dependencies.uow import get_uow
from src.infra.resource.exceptions import ResourceServerException


class UpdateDNSUseCase(BaseUseCase):
    """DNS 서브도메인을 수정하는 유즈케이스"""

    def __init__(
        self,
        uow: UnitOfWork = Depends(get_uow),
        resource_client: DNSResourceClient = Depends(get_resource_client),
    ):
        self.uow = uow
        self.resource_client = resource_client

    async def __call__(
        self,
        dns_id: int,
        request: DNSUpdate,
        user_id: int,
    ) -> DNS:
        async with self.uow:
            dns = await self.uow.dns.get_by_id(dns_id)
            if dns is None:
                raise DNSNotFound()

            if await self.uow.dns.exists_by_subdomain(request.subdomain, exclude_dns_id=dns_id):
                raise DNSAlreadyExists()

            dns = await self.uow.dns.update_subdomain(dns_id, request.subdomain)

            try:
                await self.resource_client.update(dns)
            except ResourceServerException as e:
                raise ResourceServerError() from e

            await self.uow.commit()
            return dns
