from abc import abstractmethod
from typing import List

from src.core.domain.dns import DNS
from src.core.repository.base import Repository


class DNSRepository(Repository[DNS]):
    """DNS Repository 추상 클래스"""

    @abstractmethod
    async def insert(self, dns: DNS) -> DNS:
        """DNS를 삽입합니다."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, dns_id: int) -> DNS | None:
        """ID로 DNS를 조회합니다."""
        raise NotImplementedError

    @abstractmethod
    async def list_by_project(
        self,
        project_id: int,
        limit: int,
        cursor: int | None = None,
    ) -> List[DNS]:
        """프로젝트의 DNS 목록을 조회합니다."""
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_project(self, project_id: int) -> List[DNS]:
        """프로젝트의 모든 DNS 목록을 조회합니다."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, dns: DNS) -> None:
        """DNS를 삭제합니다."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_project(self, project_id: int) -> None:
        """프로젝트의 모든 DNS를 삭제합니다."""
        raise NotImplementedError

    @abstractmethod
    async def update_subdomain(self, dns_id: int, subdomain: str) -> DNS:
        """DNS 서브도메인을 업데이트합니다."""
        raise NotImplementedError

    @abstractmethod
    async def exists_by_subdomain(
        self,
        subdomain: str,
        exclude_dns_id: int | None = None,
    ) -> bool:
        """서브도메인 중복 여부를 확인합니다."""
        raise NotImplementedError
