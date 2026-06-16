from ..backends.http import BocaClient
from pathlib import Path

class BocaAdmin(BocaClient):
    _admin_pass: str

    async def upload_problem(self, zip_path: Path) -> bool:
        # We need to find the problem number or just let BOCA assign it.
        # problem.php handles the upload.
        # We need Submit5=Send, and the file in probleminput.
        # We also need a name. Let's use the filename without extension.
        name = zip_path.stem
        
        with open(zip_path, "rb") as f:
            files = {
                "probleminput": (zip_path.name, f, "application/zip")
            }
            data = {
                "problemname": name,
                "fullname": name,
                "basename": name,
                "timelimit": "1",
                "confirmation": "confirm",
                "Submit5": "Send"
            }
            resp = await self.client.post(
                f"{self.base_url}/admin/problem.php",
                data=data,
                files=files
            )
            resp.raise_for_status()
            return "Problem imported" in resp.text or "data will be replaced" in resp.text

    async def create_team(self, username: str, password: str, fullname: str) -> None:
        # We can use the user import feature or create one by one.
        # Let's try creating one by one first for simplicity, or use the TSV import.
        # TSV import is faster for many teams.
        
        # Format for users.txt as per doc/import-user.txt:
        # [user]
        # usernumber=...
        # username=...
        # userpassword=...
        # userfullname=...
        # usertype=team
        
        # Actually, let's use the TSV format as it seems robust.
        # But wait, I need to know the next usernumber.
        # BOCA usually starts teams at 1.
        
        # Let's try a single team creation first to see if it works.
        # Looking at src/admin/user.php:
        # if (isset($_POST["username"]) && ... && $_POST["confirmation"] == "confirm")
        
        # We need the admin password to confirm.
        # No, wait. The code says:
        # if(myhash($a['userpassword'] . session_id()) != $passcheck) { ... }
        # $passcheck = $_POST["passwordo"];
        
        # So we need the admin password hash salted with session_id.
        
        # In src/admin/user.php:
        # $param['pass'] = bighexsub($_POST["passwordn1"],$a['userpassword']);
        # This is very complex. BOCA seems to use some kind of password delta?
        
        # Let's use the IMPORT feature instead. It's much simpler.
        pass

    async def import_teams(self, teams_data: str) -> bool:
        # teams_data is a string in the [user] format.
        files = {
            "importfile": ("teams.txt", teams_data, "text/plain")
        }
        data = {
            "confirmation": "confirm",
            "Submit": "Import"
        }
        resp = await self.client.post(
            f"{self.base_url}/admin/user.php",
            data=data,
            files=files
        )
        resp.raise_for_status()
        return "Users imported" in resp.text

    def set_admin_pass(self, admin_pass: str) -> None:
        self._admin_pass = admin_pass
