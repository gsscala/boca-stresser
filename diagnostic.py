import httpx
import hashlib
import asyncio
import sys

async def diagnostic(url, user, password):
    url = url.rstrip("/")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        print(f"Target: {url}")
        
        # 1. Get Session ID
        print("Step 1: Getting session ID...")
        resp = await client.get(f"{url}/index.php?getsessionid=1")
        print(f"Status: {resp.status_code}")
        session_id = resp.text.strip()
        print(f"Session ID: {session_id}")
        print(f"Cookies: {client.cookies}")
        
        # 2. Hash Password
        h1 = hashlib.sha256(password.encode()).hexdigest()
        h2 = hashlib.sha256((h1 + session_id).encode()).hexdigest()
        
        # 3. Attempt Login
        print("\nStep 2: Attempting login...")
        resp = await client.get(
            f"{url}/index.php",
            params={"name": user, "password": h2}
        )
        print(f"Status: {resp.status_code}")
        print(f"Final URL: {resp.url}")
        print(f"Final Cookies: {client.cookies}")
        
        content = resp.text
        print("\nResponse Preview (first 1000 chars):")
        print(content[:1000])
        
        import re
        redir_match = re.search(r"document\.location='([^']+)';", content)
        if redir_match:
            target = redir_match.group(1)
            print(f"\nDetected Redirection to: {target}")
            if "admin/index.php" in target:
                print("Result: ADMIN LOGIN SUCCESS")
            elif "team/index.php" in target:
                print("Result: TEAM LOGIN SUCCESS")
            else:
                print("Result: LOGIN FAILED (Redirected to unknown)")
        else:
            print("\nResult: NO REDIRECTION DETECTED")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python diagnostic.py <url> <user> <pass>")
    else:
        asyncio.run(diagnostic(sys.argv[1], sys.argv[2], sys.argv[3]))
