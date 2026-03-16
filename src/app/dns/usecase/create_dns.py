from fastapi import Depends

from src.app.base_usecase import BaseUseCase
from src.app.dns.exceptions import DNSAlreadyExists, OnlyOwnerCanManageDNS, ResourceServerError
from src.app.dns.schemas import DNSCreate
from src.common.enums import UserRole
from src.common.id_generator import IdGenerator
from src.core.client.dns_resource import DNSResourceClient
from src.core.domain.dns import DNS
from src.core.uow import UnitOfWork
from src.dependencies.resource_client import get_resource_client
from src.dependencies.uow import get_uow
from src.infra.resource.exceptions import ResourceServerException


class CreateDNSUseCase(BaseUseCase):
    """DNS를 생성하는 유즈케이스"""

    def __init__(
        self,
        uow: UnitOfWork = Depends(get_uow),
        resource_client: DNSResourceClient = Depends(get_resource_client),
    ):
        self.uow = uow
        self.resource_client = resource_client

    async def __call__(
        self,
        deployment_id: int,
        request: DNSCreate,
        user_id: int,
        role: UserRole,
    ) -> DNS:
        if role != UserRole.OWNER:
            raise OnlyOwnerCanManageDNS()

        is_auto_generated = request.subdomain is None

        async with self.uow:
            if is_auto_generated:
                for _ in range(5):
                    subdomain = str(IdGenerator.generate_sonyflake_id())
                    if not await self.uow.dns.exists_by_subdomain(subdomain):
                        break
                else:
                    raise DNSAlreadyExists()
            else:
                subdomain = request.subdomain
                if await self.uow.dns.exists_by_subdomain(subdomain):
                    raise DNSAlreadyExists()

            dns = DNS(
                project_id=request.project_id,
                deployment_id=deployment_id,
                subdomain=subdomain,
                deployment_type=request.deployment_type,
            )
            dns = await self.uow.dns.insert(dns)

            try:
                await self.resource_client.create(dns)
            except ResourceServerException as e:
                raise ResourceServerError() from e

            await self.uow.commit()
            return dns
