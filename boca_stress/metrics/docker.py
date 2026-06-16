import aiodocker
from .ssh import RemoteCollector
from typing import Any, Dict, List, Optional

class DockerCollector(RemoteCollector):
    def __init__(self, containers: List[str]) -> None:
        self.containers = containers
        self._docker: Optional[aiodocker.Docker] = None

    @property
    def docker(self) -> aiodocker.Docker:
        if self._docker is None:
            self._docker = aiodocker.Docker()
        return self._docker

    async def collect(self) -> Dict[str, Any]:
        results = {}
        try:
            for container_name in self.containers:
                try:
                    container = await self.docker.containers.get(container_name)
                    stats = await container.stats(stream=False)
                    # Stats is a list of 1 element when stream=False
                    stat = stats[0]
                    
                    # Basic CPU/Mem calculation
                    cpu_delta = stat['cpu_stats']['cpu_usage']['total_usage'] - \
                                stat['precpu_stats']['cpu_usage']['total_usage']
                    system_delta = stat['cpu_stats']['system_cpu_usage'] - \
                                   stat['precpu_stats']['system_cpu_usage']
                    
                    cpu_percent = 0.0
                    if system_delta > 0.0 and cpu_delta > 0.0:
                        cpu_percent = (cpu_delta / system_delta) * len(stat['cpu_stats']['cpu_usage']['percpu_usage']) * 100.0
                    
                    mem_usage = stat['memory_stats']['usage']
                    mem_limit = stat['memory_stats']['limit']
                    mem_percent = (mem_usage / mem_limit) * 100.0
                    
                    results[container_name] = {
                        "cpu": cpu_percent,
                        "mem": mem_percent
                    }
                except Exception:
                    continue
        except Exception:
            pass
        return {"containers": results}

    async def close(self):
        if self._docker:
            await self._docker.close()
            self._docker = None
