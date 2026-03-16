from sqlalchemy import BigInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.common.id_generator import IdGenerator
from src.core.db import BaseEntity
from src.core.domain.dns import DNS as DNSEntity


class DNS(BaseEntity):
    __tablename__ = "dns"
    __table_args__ = (
        UniqueConstraint(
            "subdomain",
            name="uq_dns_subdomain",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        default=IdGenerator.generate_sonyflake_id,
    )
    project_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
    )
    deployment_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
    )
    subdomain: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    def to_entity(self) -> DNSEntity:
        return DNSEntity(
            id=self.id,
            project_id=self.project_id,
            deployment_id=self.deployment_id,
            subdomain=self.subdomain,
        )
