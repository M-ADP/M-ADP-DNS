from dataclasses import dataclass, field

from src.common.id_generator import IdGenerator


@dataclass
class DNS:
    id: int = field(default_factory=IdGenerator.generate_sonyflake_id)
    project_id: int = 0
    deployment_id: int = 0
    subdomain: str = ""

    def update_subdomain(self, subdomain: str) -> None:
        self.subdomain = subdomain
