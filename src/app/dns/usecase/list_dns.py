from fastapi import Depends

from src.app.base_usecase import BaseUseCase
from src.common.schemas import CursorPage
from src.core.domain.dns import DNS
from src.core.uow import UnitOfWork
from src.dependencies.uow import get_uow

DEFAULT_LIMIT = 20


class ListDNSUseCase(BaseUseCase):
    """프로젝트의 DNS 목록을 조회하는 유즈케이스"""

    def __init__(self, uow: UnitOfWork = Depends(get_uow)):
        self.uow = uow

    async def __call__(
        self,
        project_id: int,
        user_id: int,
        limit: int = DEFAULT_LIMIT,
        cursor: int | None = None,
    ) -> CursorPage[DNS]:
        async with self.uow:
            items = await self.uow.dns.list_by_project(
                project_id=project_id,
                limit=limit + 1,
                cursor=cursor,
            )
            next_cursor: int | None = None
            if len(items) > limit:
                items = items[:limit]
                next_cursor = items[-1].id
            return CursorPage(cursor=next_cursor, items=items)
