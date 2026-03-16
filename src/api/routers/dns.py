from fastapi import APIRouter, Depends, Query

from src.app.dns.schemas import DNSCreate, DNSResponse, DNSUpdate
from src.app.dns.usecase import (
    CreateDNSUseCase,
    DeleteDNSUseCase,
    ListDNSUseCase,
    UpdateDNSUseCase,
)
from src.common.schemas import CursorPage, SuccessResponse
from src.dependencies.auth import UserInfo, get_user_info

router = APIRouter(prefix="/dns", tags=["dns"])


@router.post(
    "/{deployment_id}",
    response_model=SuccessResponse[DNSResponse],
    status_code=201,
)
async def create_dns_endpoint(
    deployment_id: int,
    payload: DNSCreate,
    user: UserInfo = Depends(get_user_info),
    usecase: CreateDNSUseCase = Depends(CreateDNSUseCase),
) -> SuccessResponse[DNSResponse]:
    """DNS를 생성합니다. (PROJECT OWNER 전용)"""
    dns = await usecase(
        deployment_id=deployment_id,
        request=payload,
        user_id=user.user_id,
        role=user.role,
    )
    return SuccessResponse(
        message="DNS가 생성되었습니다.",
        data=DNSResponse.model_validate(dns),
    )


@router.put(
    "/{dns_id}",
    response_model=SuccessResponse[DNSResponse],
    status_code=200,
)
async def update_dns_endpoint(
    dns_id: int,
    payload: DNSUpdate,
    user: UserInfo = Depends(get_user_info),
    usecase: UpdateDNSUseCase = Depends(UpdateDNSUseCase),
) -> SuccessResponse[DNSResponse]:
    """DNS 서브도메인을 수정합니다. (PROJECT OWNER 전용)"""
    dns = await usecase(
        dns_id=dns_id,
        request=payload,
        user_id=user.user_id,
        role=user.role,
    )
    return SuccessResponse(
        message="DNS가 수정되었습니다.",
        data=DNSResponse.model_validate(dns),
    )


@router.delete(
    "/{dns_id}",
    response_model=SuccessResponse[DNSResponse],
    status_code=200,
)
async def delete_dns_endpoint(
    dns_id: int,
    user: UserInfo = Depends(get_user_info),
    usecase: DeleteDNSUseCase = Depends(DeleteDNSUseCase),
) -> SuccessResponse[DNSResponse]:
    """DNS를 삭제합니다. (PROJECT OWNER 전용)"""
    dns = await usecase(
        dns_id=dns_id,
        user_id=user.user_id,
        role=user.role,
    )
    return SuccessResponse(
        message="DNS가 삭제되었습니다.",
        data=DNSResponse.model_validate(dns),
    )


@router.get(
    "/{project_id}",
    response_model=SuccessResponse[CursorPage[DNSResponse]],
    status_code=200,
)
async def list_dns_endpoint(
    project_id: int,
    cursor: int | None = Query(
        None,
        description="다음 페이지 커서(id). 지정하면 해당 커서 이전부터 조회 (내림차순)",
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="한 번에 가져올 DNS 수 (1~100, 기본 20)",
    ),
    user: UserInfo = Depends(get_user_info),
    usecase: ListDNSUseCase = Depends(ListDNSUseCase),
) -> SuccessResponse[CursorPage[DNSResponse]]:
    """프로젝트의 DNS 목록을 조회합니다."""
    page = await usecase(
        project_id=project_id,
        user_id=user.user_id,
        limit=limit,
        cursor=cursor,
    )
    return SuccessResponse(
        message="DNS 목록을 조회했습니다.",
        data=CursorPage(
            cursor=page.cursor,
            items=[DNSResponse.model_validate(dns) for dns in page.items],
        ),
    )
