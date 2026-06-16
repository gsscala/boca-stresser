import asyncssh
from typing import Any, Dict, Optional

class RemoteCollector:
    async def collect(self) -> Dict[str, Any]:
        return {}

class SSHCollector(RemoteCollector):
    def __init__(self, host: str, user: str, password: str, db_container: Optional[str] = None) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.db_container = db_container

    async def collect(self) -> Dict[str, Any]:
        try:
            async with asyncssh.connect(
                self.host, username=self.user, password=self.password, known_hosts=None
            ) as conn:
                # ... existing metrics collection ...
                result = await conn.run("top -bn1 | grep 'Cpu(s)'", check=True)
                cpu_line = result.stdout.strip()
                cpu_usage = 0.0
                try:
                    idle = float(cpu_line.split("id")[0].split(",")[-1].strip())
                    cpu_usage = 100.0 - idle
                except (ValueError, IndexError):
                    pass

                result = await conn.run("free -m", check=True)
                mem_lines = result.stdout.splitlines()
                mem_usage = 0.0
                if len(mem_lines) > 1:
                    parts = mem_lines[1].split()
                    total = int(parts[1])
                    used = int(parts[2])
                    mem_usage = (used / total) * 100

                result = await conn.run("uptime", check=True)
                load = [0.0, 0.0, 0.0]
                try:
                    load_part = result.stdout.split("load average:")[1].strip()
                    load = [float(x.strip()) for x in load_part.split(",")]
                except (ValueError, IndexError):
                    pass

                queue_size = 0
                if self.db_container:
                    # Query DB via docker exec
                    db_cmd = f"docker exec {self.db_container} psql -U bocauser -d bocadb -t -c \"SELECT count(*) FROM runtable WHERE runstatus ~* 'open' OR runstatus IS NULL\""
                    db_res = await conn.run(db_cmd)
                    if db_res.exit_status == 0:
                        try:
                            queue_size = int(db_res.stdout.strip())
                        except ValueError:
                            pass

                data = {
                    "cpu": cpu_usage,
                    "mem": mem_usage,
                    "load": load,
                    "host": self.host
                }
                if self.db_container:
                    data["queue_size"] = queue_size
                
                return data
        except Exception:
            return {}
