import httpx
import hashlib
from typing import Optional, Any, Self

class BocaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=30.0)
        self.session_id: Optional[str] = None

    async def get_session_id(self) -> str:
        resp = await self.client.get(f"{self.base_url}/index.php?getsessionid=1")
        resp.raise_for_status()
        self.session_id = resp.text.strip()
        return self.session_id

    def hash_password(self, password: str, session_id: str) -> str:
        h1 = hashlib.sha256(password.encode()).hexdigest()
        h2 = hashlib.sha256((h1 + session_id).encode()).hexdigest()
        return h2

    async def login(self, username: str, password: str) -> bool:
        session_id = await self.get_session_id()
        pass_hash = self.hash_password(password, session_id)
        
        resp = await self.client.get(
            f"{self.base_url}/index.php",
            params={"name": username, "password": pass_hash}
        )
        resp.raise_for_status()
        # BOCA redirects to index.php if login fails, or to some other page if it succeeds.
        # Usually, if we are in admin/, it means we logged in as admin.
        # We can check if the response content contains indicators of a successful login.
        if "Login" in resp.text and "password" in resp.text:
            return False
        return True

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
