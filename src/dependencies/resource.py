from src.core.client.dns_resource import DNSResourceClient, FakeDNSResourceClient


async def get_resource_client() -> DNSResourceClient:
    return FakeDNSResourceClient()