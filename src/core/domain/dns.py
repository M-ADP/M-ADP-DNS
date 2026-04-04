from dataclasses import dataclass, field
from typing import Literal

from src.common.id_generator import IdGenerator

DeploymentType = Literal["CloudDB", "App Deployment"]
ServiceType = Literal["http", "ssh"]


@dataclass
class DNS:
    id: int = field(default_factory=IdGenerator.generate_sonyflake_id)
    project_id: int = 0
    deployment_id: int = 0
    subdomain: str = ""
    deployment_type: DeploymentType = "App Deployment"
    service_type: ServiceType = "http"

    def update_subdomain(self, subdomain: str) -> None:
        self.subdomain = subdomain
