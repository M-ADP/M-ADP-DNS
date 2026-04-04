from dataclasses import dataclass

from fastapi import Header, HTTPException, status

from src.common.enums import UserRole


@dataclass
class UserInfo:
    user_id: int
    role: UserRole


async def get_user_info(
    x_user_id: int = Header(..., alias="X-User-Id", description="사용자 ID"),
    x_user_role: UserRole = Header(..., alias="X-User-Role", description="사용자 역할 (ADMIN | USER)"),
) -> UserInfo:
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 정보가 없습니다.",
        )
    return UserInfo(user_id=x_user_id, role=x_user_role)
