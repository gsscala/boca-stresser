from ..backends.http import BocaClient
from pathlib import Path
import re
import hashlib

class BocaAdmin(BocaClient):
    _admin_pass: str
    _admin_user: str
    site_number: str = "1"
    contest_number: str = "0"

    async def login(self, username: str, password: str) -> bool:
        success = await super().login(username, password)
        if success:
            # Hit admin/index.php to get context
            resp = await self.client.get(f"{self.base_url}/admin/index.php")
            import re
            match = re.search(r"\(site=(\d+)\)", resp.text)
            if match:
                self.site_number = match.group(1)
            
            # Contest number is often in the session or in index.php source
            # But let's just assume we are in the active one.
            print(f"DEBUG: Logged in as admin (Site: {self.site_number})")
        return success

    async def upload_problem(self, zip_path: Path, problem_number: int) -> bool:
        name = zip_path.stem
        
        async def _attempt_upload():
            with open(zip_path, "rb") as f:
                files = {
                    "probleminput": (zip_path.name, f, "application/zip")
                }
                data = {
                    "problemnumber": str(problem_number),
                    "problemname": name,
                    "colorname": "White",
                    "color": "ffffff",
                    "autojudge_new_sel": "all",
                    "confirmation": "confirm",
                    "Submit3": "Send"
                }
                resp = await self.client.post(
                    f"{self.base_url}/admin/problem.php",
                    data=data,
                    files=files
                )
                resp.raise_for_status()
                return resp

        resp = await _attempt_upload()
        
        if "Session expired" in resp.text:
            if await self.login(self._admin_user, self._admin_pass):
                resp = await _attempt_upload()
            else:
                return False

        # Verify if BOCA accepted the request
        error_match = re.search(r"alert\('([^']+)'\)", resp.text)
        if error_match:
            print(f"DEBUG: Problem upload failed for {name} (#{problem_number}): {error_match.group(1)}")
            return False
            
        if "document.location='problem.php'" in resp.text:
            return True
            
        if re.search(rf"\b{name}\b", resp.text):
            return True
            
        print(f"DEBUG: Problem upload failed for {name} (#{problem_number}): Unknown response state")
        return False

    def big_hex_soma(self, hex1: str, hex2: str) -> str:
        # Match BOCA's bighexsoma from hex.php
        if len(hex1) > len(hex2):
            hex1, hex2 = hex2, hex1
        hex1 = hex1.zfill(len(hex2))
        
        sobra = 0
        resultado = ""
        for i in range(len(hex1)-1, -1, -1):
            op1 = int(hex1[i], 16)
            op2 = int(hex2[i], 16)
            r = op1 + op2 + sobra
            if r > 15:
                r -= 16
                sobra = 1
            else:
                sobra = 0
            resultado = hex(r)[2:] + resultado
        
        if sobra == 1:
            resultado = "1" + resultado
        return resultado

    async def import_teams(self, teams_count: int) -> bool:
        # Single-user creation is more reliable than bulk import in some BOCA versions
        # We'll create teams one by one.
        admin_pass_hash = hashlib.sha256(self._admin_pass.encode()).hexdigest()
        
        for i in range(1, teams_count + 1):
            name = f"team{i:03d}"
            # password will be the same as name
            new_pass_hash = hashlib.sha256(name.encode()).hexdigest()
            
            # passwordn1 = bighexsoma(sha256(new_pass), sha256(admin_pass))
            pass_n1 = self.big_hex_soma(new_pass_hash, admin_pass_hash)
            
            if not self.session_id:
                await self.get_session_id()
            
            pass_o = hashlib.sha256((admin_pass_hash + self.session_id).encode()).hexdigest()
            
            data = {
                "usersitenumber": self.site_number,
                "usernumber": str(i),
                "username": name,
                "usericpcid": name,
                "usertype": "team",
                "userenabled": "t",
                "usermultilogin": "t",
                "userfullname": f"Team {i}",
                "userdesc": f"Team {i}",
                "userip": "",
                "passwordn1": pass_n1,
                "passwordn2": pass_n1,
                "changepass": "t",
                "passwordo": pass_o,
                "confirmation": "confirm",
                "Submit": "Send"
            }
            
            print(f"Creating team {name}...", end="\r")
            resp = await self.client.post(f"{self.base_url}/admin/user.php", data=data)
            resp.raise_for_status()
            
            if "Session expired" in resp.text:
                await self.login(self._admin_user, self._admin_pass)
                # Refresh pass_o with new session_id
                pass_o = hashlib.sha256((admin_pass_hash + self.session_id).encode()).hexdigest() if self.session_id else pass_o
                data["passwordo"] = pass_o
                # Retry once
                resp = await self.client.post(f"{self.base_url}/admin/user.php", data=data)
                resp.raise_for_status()

            # Check for error alerts
            error_match = re.search(r"alert\('([^']+)'\)", resp.text)
            if error_match:
                print(f"\nDEBUG: Failed to create team {name}: {error_match.group(1)}")
                return False
                
            # Check for redirect to user.php or presence of name
            if "document.location='user.php'" in resp.text or name in resp.text:
                continue
                
            print(f"\nDEBUG: Failed to create team {name}: Unknown response state")
            return False
        
        print(f"\nSuccessfully created {teams_count} teams.")
        return True

    def set_admin_credentials(self, username: str, admin_pass: str) -> None:
        self._admin_user = username
        self._admin_pass = admin_pass

    def set_admin_pass(self, admin_pass: str) -> None:
        self._admin_pass = admin_pass
