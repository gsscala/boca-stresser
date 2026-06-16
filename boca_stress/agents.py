import asyncio
import random
from pathlib import Path
from typing import Optional, Dict
from .boca.team import BocaTeam
from .models import SolutionsConfig
from .metrics.collector import MetricsCollector
import time

class TeamAgent:
    def __init__(
        self,
        agent_id: int,
        url: str,
        username: str,
        password: str,
        config: SolutionsConfig,
        solutions_dir: Path,
        status_prob: float,
        max_think_secs: int,
        metrics_collector: MetricsCollector
    ) -> None:
        self.agent_id = agent_id
        self.url = url
        self.username = username
        self.password = password
        self.config = config
        self.solutions_dir = solutions_dir
        self.status_prob = status_prob
        self.max_think_secs = max_think_secs
        self.metrics = metrics_collector
        self.client: Optional[BocaTeam] = None
        self.problem_ids: Dict[str, str] = {}
        self.language_ids: Dict[str, str] = {}
        self.pending_runs: Dict[str, float] = {} # run_id -> submission_time

    async def run(self, stop_event: asyncio.Event) -> None:
        async with BocaTeam(self.url) as client:
            self.client = client
            if not await client.login(self.username, self.password):
                self.metrics.register_error(self.agent_id, "Login failed")
                return

            # Refresh metadata only if missing (Simulator should have pre-populated)
            if not self.problem_ids:
                self.problem_ids = await client.get_problems()
            if not self.language_ids:
                self.language_ids = await client.get_languages()

            while not stop_event.is_set():
                think_time = random.randint(1, self.max_think_secs)
                await asyncio.sleep(think_time)

                if stop_event.is_set():
                    break

                try:
                    if random.random() < self.status_prob:
                        await self.view_status()
                    else:
                        await self.submit_solution()
                except Exception as e:
                    self.metrics.register_error(self.agent_id, str(e))

    async def view_status(self) -> None:
        if not self.client:
            return
        start = time.perf_counter()
        runs = await self.client.view_status()
        latency = (time.perf_counter() - start) * 1000
        self.metrics.register_status_view(self.agent_id, latency)

        # Check for finished runs
        now = time.time()
        for run in runs:
            rid = run["id"]
            # Map pending submissions to actual run IDs
            if rid not in self.pending_runs:
                # If we see a new run ID and we have an anonymous "pending" entry
                anon_keys = [k for k in self.pending_runs.keys() if k.startswith("pending_")]
                if anon_keys:
                    oldest_anon = min(anon_keys)
                    self.pending_runs[rid] = self.pending_runs.pop(oldest_anon)
            
            if rid in self.pending_runs and run["judged"]:
                sub_time = self.pending_runs.pop(rid)
                judging_latency = (now - sub_time) * 1000
                self.metrics.register_judging_latency(self.agent_id, judging_latency)

    async def submit_solution(self) -> None:
        if not self.client:
            return
        
        # Ensure we have problems, otherwise try to refresh
        if not self.problem_ids:
            self.problem_ids = await self.client.get_problems()
        if not self.language_ids:
            self.language_ids = await self.client.get_languages()

        # Weighted choice of problem
        problems = list(self.config.problems.keys())
        if not problems:
            return
        weights = [self.config.problems[p].weight for p in problems]
        problem_name = random.choices(problems, weights=weights)[0]
        
        problem_cfg = self.config.problems[problem_name]
        
        # Weighted choice of solution
        sol_weights = [s.weight for s in problem_cfg.solutions]
        solution = random.choices(problem_cfg.solutions, weights=sol_weights)[0]
        
        # Broad fuzzy match problem
        problem_id = None
        for name, pid in self.problem_ids.items():
            # Match if problem_name ("A") is exactly the short name, 
            # or if it appears in the full name ("1 - A - Fullname")
            p_name_lower = problem_name.lower()
            full_name_lower = name.lower()
            # Split by common BOCA delimiters
            parts = [p.strip().lower() for p in name.replace('-', ' ').replace('.', ' ').split()]
            
            if p_name_lower == full_name_lower or p_name_lower in parts or f" {p_name_lower} " in f" {full_name_lower} ":
                problem_id = pid
                break
        
        if not problem_id:
            found = list(self.problem_ids.keys())[:5]
            self.metrics.register_error(self.agent_id, f"Problem {problem_name} not found. Found: {found}")
            return

        # Broad fuzzy match language
        language_id = None
        for name, lid in self.language_ids.items():
            if solution.language.lower() in name.lower():
                language_id = lid
                break
        
        if not language_id:
            if self.language_ids:
                language_id = list(self.language_ids.values())[0]
            else:
                self.metrics.register_error(self.agent_id, f"No languages available on server")
                return

        source_path = self.solutions_dir / solution.file
        if not source_path.exists():
            self.metrics.register_error(self.agent_id, f"Source file {solution.file} not found")
            return
        
        start = time.perf_counter()
        # Use improved submission method with server feedback
        success, msg = await self.client.submit_run_with_msg(problem_id, language_id, source_path)
        latency = (time.perf_counter() - start) * 1000
        
        if success:
            self.pending_runs["pending_" + str(time.time())] = time.time()
            self.metrics.register_submission(self.agent_id, problem_name, solution.language, latency)
        else:
            self.metrics.register_error(self.agent_id, f"Sub failed for {problem_name}: {msg}")
