from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

DeploymentType = Literal["CloudDB", "App Deployment"]
ServiceType = Literal["http"]


class DNSCreate(BaseModel):
    project_id: int = Field(..., description="프로젝트 ID")
    deployment_type: DeploymentType = Field(..., description="배포 타입")
    service_type: ServiceType = Field(
        "http",
        description="서비스 타입 (http)",
        examples=["http"],
    )
    subdomain: Optional[str] = Field(
        None,
        min_length=1,
        max_length=63,
        description="서브도메인 (영문 소문자, 숫자, 하이픈만 허용). 미입력 시 자동 생성",
        examples=["my-app"],
    )

    @field_validator("subdomain")
    @classmethod
    def validate_subdomain(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        import re
        v = v.strip().lower()
        if not re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", v):
            raise ValueError("서브도메인은 영문 소문자, 숫자, 하이픈만 사용 가능하며 하이픈으로 시작하거나 끝날 수 없습니다.")
        return v


class DNSUpdate(BaseModel):
    subdomain: str = Field(
        ...,
        min_length=1,
        max_length=63,
        description="변경할 서브도메인",
        examples=["new-app"],
    )

    @field_validator("subdomain")
    @classmethod
    def validate_subdomain(cls, v: str) -> str:
        import re
        v = v.strip().lower()
        if not re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", v):
            raise ValueError("서브도메인은 영문 소문자, 숫자, 하이픈만 사용 가능하며 하이픈으로 시작하거나 끝날 수 없습니다.")
        return v


class DNSResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    deployment_id: int
    subdomain: str
    deployment_type: DeploymentType
    service_type: ServiceType
