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

    async def submit_run_with_msg(self, problem_id: str, language_id: str, source_path: Path) -> tuple[bool, str]:
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
            text = resp.text
            
            # Successful submission indicators
            # "YOU GOT NEWS" means BOCA is just notifying about a previous judgment
            # which usually happens alongside or instead of the "Run submitted" message
            success_markers = [
                "Run submitted", "Wait for a moment", "submetido com sucesso", 
                "aguarde um momento", "YOU GOT NEWS", "VOCE TEM NOTICIAS"
            ]
            
            if any(m.lower() in text.lower() for m in success_markers):
                return True, ""
            
            # If we are on run.php and there is no obvious error/alert, it's likely a success
            if "/run.php" in str(resp.url) and "alert(" not in text and "invalid" not in text.lower():
                return True, ""

            # Extract potential error from alert() or similar
            if "alert(" in text:
                msg = text.split("alert(")[1].split(")")[0].strip("'\"")
                return False, msg
            
            return False, text[:50].replace("\n", " ")

    async def submit_run(self, problem_id: str, language_id: str, source_path: Path) -> bool:
        success, _ = await self.submit_run_with_msg(problem_id, language_id, source_path)
        return success

    async def view_status(self) -> list[dict]:
        resp = await self.client.get(f"{self.base_url}/team/run.php")
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table", {"border": "1"})
        runs = []
        if not table:
            return runs

        rows = table.find_all("tr")
        if not rows:
            return runs

        # Find header indices
        headers = [th.text.strip().lower() for th in rows[0].find_all(["td", "th"])]
        
        def find_idx(names: list[str]) -> int:
            for name in names:
                for i, h in enumerate(headers):
                    if name in h: return i
            return -1

        run_idx = find_idx(["run", "id", "#"])
        status_idx = find_idx(["status", "situacao", "estado"])
        answer_idx = find_idx(["answer", "resposta", "resultado"])

        # Default to common indices if headers not found
        if run_idx == -1: run_idx = 0
        if answer_idx == -1: answer_idx = 4
        
        # Skip header row
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) > max(run_idx, answer_idx, status_idx):
                run_id = cols[run_idx].text.strip()
                
                # Check Answer first, then Status
                ans_text = cols[answer_idx].text.strip().lower() if answer_idx != -1 else ""
                stat_text = cols[status_idx].text.strip().lower() if status_idx != -1 else ""
                
                # A run is judged if there is a non-waiting verdict in either column
                waiting_terms = ["", "not judged", "not answered", "waiting", "aguardando", "processando"]
                judged = any(ans_text and w not in ans_text for w in waiting_terms) or \
                         any(stat_text and "judged" in stat_text or "finalizado" in stat_text for _ in [1])

                runs.append({
                    "id": run_id,
                    "judged": judged,
                    "status": ans_text or stat_text
                })
        return runs
