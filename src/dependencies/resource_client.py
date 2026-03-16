from src.common.config.settings import get_resource_server_config
from src.core.client.dns_resource import DNSResourceClient
from src.infra.resource.dns_resource_client import DNSResourceClientImpl


def get_resource_client() -> DNSResourceClient:
    config = get_resource_server_config()
    return DNSResourceClientImpl(base_url=config.base_url)
