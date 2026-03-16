from fastapi import status

from src.core.exceptions import AppException


class ResourceServerError(AppException):
    def __init__(self) -> None:
        super().__init__(
            "리소스 서버와 통신 중 오류가 발생했습니다.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="RESOURCE_SERVER_ERROR",
        )


class DNSNotFound(AppException):
    def __init__(self) -> None:
        super().__init__(
            "DNS를 찾을 수 없습니다.",
            status_code=status.HTTP_404_NOT_FOUND,
            code="DNS_NOT_FOUND",
        )


class DNSAlreadyExists(AppException):
    def __init__(self) -> None:
        super().__init__(
            "이미 사용 중인 서브도메인입니다.",
            status_code=status.HTTP_409_CONFLICT,
            code="DNS_SUBDOMAIN_ALREADY_EXISTS",
        )


class OnlyOwnerCanManageDNS(AppException):
    def __init__(self) -> None:
        super().__init__(
            "프로젝트 소유자만 DNS를 관리할 수 있습니다.",
            status_code=status.HTTP_403_FORBIDDEN,
            code="ONLY_OWNER_CAN_MANAGE_DNS",
        )
