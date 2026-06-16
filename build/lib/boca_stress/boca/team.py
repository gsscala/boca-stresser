from ..backends.http import BocaClient
from pathlib import Path
from typing import Dict
from bs4 import BeautifulSoup

class BocaTeam(BocaClient):
    async def get_problems(self) -> Dict[str, str]:
        """Returns a map from problem name to its ID."""
        resp = await self.client.get(f"{self.base_url}/team/run.php")
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, "html.parser")
        select = soup.find("select", {"name": "problem"})
        problems: Dict[str, str] = {}
        if select and hasattr(select, "find_all"):
            for option in select.find_all("option"):
                val = option.get("value")
                if val and isinstance(val, str):
                    problems[option.text.strip()] = val
        return problems

    async def get_languages(self) -> Dict[str, str]:
        """Returns a map from language name to its ID."""
        resp = await self.client.get(f"{self.base_url}/team/run.php")
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, "html.parser")
        select = soup.find("select", {"name": "language"})
        languages: Dict[str, str] = {}
        if select and hasattr(select, "find_all"):
            for option in select.find_all("option"):
                val = option.get("value")
                if val and isinstance(val, str):
                    languages[option.text.strip()] = val
        return languages

    async def submit_run(self, problem_id: str, language_id: str, source_path: Path) -> bool:
        with open(source_path, "rb") as f:
            files = {
                "sourcefile": (source_path.name, f, "text/plain")
            }
            data = {
                "problem": problem_id,
                "language": language_id,
                "confirmation": "confirm",
                "Submit": "Send"
            }
            resp = await self.client.post(
                f"{self.base_url}/team/run.php",
                data=data,
                files=files
            )
            resp.raise_for_status()
            return "Run submitted" in resp.text or "Wait for a moment" in resp.text

    async def view_status(self) -> str:
        resp = await self.client.get(f"{self.base_url}/team/run.php")
        resp.raise_for_status()
        return resp.text
