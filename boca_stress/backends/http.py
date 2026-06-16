import httpx
import hashlib
from typing import Optional, Any, Self

class BocaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.client = httpx.AsyncClient(follow_redirects=True, timeout=300.0, headers=headers)
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
        # 1. Get Session ID
        try:
            session_id = await self.get_session_id()
        except Exception:
            return False
            
        if not session_id:
            return False

        pass_hash = self.hash_password(password, session_id)
        
        # 2. Attempt login
        try:
            resp = await self.client.get(
                f"{self.base_url}/index.php",
                params={"name": username, "password": pass_hash}
            )
            resp.raise_for_status()
        except Exception:
            return False
        
        content = resp.text

        if "admin/index.php" in content or "team/index.php" in content:
            return True
        if "staff/index.php" in content or "judge/index.php" in content:
            return True
            
        if "/index.php" not in str(resp.url) and "/boca/index.php" not in str(resp.url):
            return True
            
        if "Logout" in content or "Log out" in content:
            return True
            
        return False

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
