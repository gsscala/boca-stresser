from .ssh import RemoteCollector
from typing import Any, Dict

class PostgresCollector(RemoteCollector):
    def __init__(self, host: str, user: str, password: str) -> None:
        self.host = host
        self.user = user
        self.password = password

    async def collect(self) -> Dict[str, Any]:
        # Implementation for PG metrics (e.g. autojudge queue size)
        return {"queue_size": 0}
