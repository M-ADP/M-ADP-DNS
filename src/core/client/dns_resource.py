from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dns import DNS


class DNSResourceClient(ABC):
    """DNS 리소스 서버 클라이언트 추상 인터페이스"""

    @abstractmethod
    async def create(self, dns: DNS) -> None:
        """DNS 레코드를 리소스 서버에 생성합니다."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, dns: DNS) -> None:
        """DNS 레코드를 리소스 서버에서 삭제합니다."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, dns: DNS) -> None:
        """DNS 레코드를 리소스 서버에서 업데이트합니다."""
        raise NotImplementedError

    @abstractmethod
    async def list_by_project(self, project_id: int) -> List[DNS]:
        """프로젝트의 DNS 레코드 목록을 리소스 서버에서 조회합니다."""
        raise NotImplementedError

class FakeDNSResourceClient(DNSResourceClient):
    async def create(self, dns: DNS) -> None:
        print("DNS 리소스 생성")

    async def delete(self, dns: DNS) -> None:
        print("DNS 리소스 삭제")

    async def update(self, dns: DNS) -> None:
        print("DNS 리소스 업데이트")

    async def list_by_project(self, project_id: int) -> List[DNS]:
        return [
            DNS(
                id=1,
            ),
            DNS(
                id=2,
            )
        ]