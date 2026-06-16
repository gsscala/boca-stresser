from typing import Any, Dict

class RemoteCollector:
    async def collect(self) -> Dict[str, Any]:
        return {}

class SSHCollector(RemoteCollector):
    def __init__(self, host: str, user: str, password: str) -> None:
        self.host = host
        self.user = user
        self.password = password

    async def collect(self) -> Dict[str, Any]:
        # Implementation for SSH metrics collection
        return {"cpu": 0, "mem": 0, "load": [0,0,0]}
