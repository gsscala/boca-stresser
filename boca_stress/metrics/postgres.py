import asyncpg
from .ssh import RemoteCollector
from typing import Any, Dict

class PostgresCollector(RemoteCollector):
    def __init__(self, host: str, user: str, password: str) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.conn = None

    async def collect(self) -> Dict[str, Any]:
        try:
            if not self.conn:
                self.conn = await asyncpg.connect(
                    user=self.user,
                    password=self.password,
                    database="bocadb",  # Default BOCA DB name
                    host=self.host
                )
            
            # Query queue size (runs not yet judged)
            # In BOCA, runs waiting for judging have runstatus starting with 'open' or null
            row = await self.conn.fetchrow(
                "SELECT count(*) FROM runtable WHERE runstatus ~* 'open' OR runstatus IS NULL"
            )
            queue_size = row['count'] if row else 0
            
            return {"queue_size": queue_size}
        except Exception:
            self.conn = None # Reset on error to retry connection
            return {"queue_size": 0}

    async def close(self):
        if self.conn:
            await self.conn.close()
            self.conn = None
