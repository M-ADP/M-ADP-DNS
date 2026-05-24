import logging

from fastapi import Depends

from src.app.base_usecase import BaseUseCase
from src.app.dns.exceptions import ResourceServerError
from src.core.client.dns_resource import DNSResourceClient
from src.core.uow import UnitOfWork
from src.dependencies.resource_client import get_resource_client
from src.dependencies.uow import get_uow
from src.infra.resource.exceptions import ResourceNotFoundException, ResourceServerException

logger = logging.getLogger(__name__)


class DeleteProjectDNSUseCase(BaseUseCase):
    """프로젝트의 모든 DNS를 삭제하는 유즈케이스"""

    def __init__(
        self,
        uow: UnitOfWork = Depends(get_uow),
        resource_client: DNSResourceClient = Depends(get_resource_client),
    ):
        self.uow = uow
        self.resource_client = resource_client

    async def __call__(
        self,
        project_id: int,
        user_id: int,
    ) -> None:
        async with self.uow:
            # 1. 프로젝트의 모든 DNS 조회
            dns_list = await self.uow.dns.get_all_by_project(project_id)
            if not dns_list:
                return

            # 2. 리소스 서버에서 삭제
            # 한 번에 여러 개를 삭제하는 API가 없으므로 루프를 돕니다.
            for dns in dns_list:
                try:
                    await self.resource_client.delete(dns)
                except ResourceNotFoundException:
                    logger.warning("리소스 서버에서 DNS를 찾을 수 없음 (무시): dns_id=%s", dns.id)
                except ResourceServerException as e:
                    logger.error("프로젝트 DNS 일괄 삭제 중 리소스 서버 오류: project_id=%s dns_id=%s", project_id, dns.id, exc_info=True)
                    raise ResourceServerError() from e

            # 3. 데이터베이스에서 일괄 삭제
            await self.uow.dns.delete_by_project(project_id)

            await self.uow.commit()
