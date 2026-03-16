from sonyflake import SonyFlake

from src.common.config.settings import get_sonyflake_config

_sf: SonyFlake | None = None


def _get_sonyflake() -> SonyFlake:
    global _sf
    if _sf is None:
        config = get_sonyflake_config()
        _sf = SonyFlake(machine_id=lambda: config.machine_id)
    return _sf


class IdGenerator:
    @staticmethod
    def generate_sonyflake_id() -> int:
        return _get_sonyflake().next_id()
