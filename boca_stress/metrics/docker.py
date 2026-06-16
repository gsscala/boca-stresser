from .ssh import RemoteCollector
from typing import Any, Dict, List

class DockerCollector(RemoteCollector):
    def __init__(self, containers: List[str]) -> None:
        self.containers = containers

    async def collect(self) -> Dict[str, Any]:
        # Implementation for Docker stats
        return {}
