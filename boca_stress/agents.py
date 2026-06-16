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

    async def run(self, stop_event: asyncio.Event) -> None:
        async with BocaTeam(self.url) as client:
            self.client = client
            if not await client.login(self.username, self.password):
                self.metrics.register_error(self.agent_id, "Login failed")
                return

            self.problem_ids = await client.get_problems()
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
        await self.client.view_status()
        latency = (time.perf_counter() - start) * 1000
        self.metrics.register_status_view(self.agent_id, latency)

    async def submit_solution(self) -> None:
        if not self.client:
            return
        # Weighted choice of problem
        problems = list(self.config.problems.keys())
        weights = [self.config.problems[p].weight for p in problems]
        problem_name = random.choices(problems, weights=weights)[0]
        
        problem_cfg = self.config.problems[problem_name]
        
        # Weighted choice of solution
        sol_weights = [s.weight for s in problem_cfg.solutions]
        solution = random.choices(problem_cfg.solutions, weights=sol_weights)[0]
        
        # Fuzzy match problem
        problem_id = None
        for name, pid in self.problem_ids.items():
            # Matches "A" with "1 - A" or "A - Alimente..."
            if problem_name.lower() in name.lower():
                problem_id = pid
                break
        
        # Fuzzy match language
        language_id = None
        for name, lid in self.language_ids.items():
            if solution.language.lower() in name.lower():
                language_id = lid
                break
        
        # Fallback for language if C++ not found (use first available)
        if not language_id and self.language_ids:
            language_id = list(self.language_ids.values())[0]

        if not problem_id:
            # Skip if problem not on server (e.g. upload failed)
            return

        if not language_id:
            self.metrics.register_error(self.agent_id, f"Language {solution.language} not found")
            return

        source_path = self.solutions_dir / solution.file
        if not source_path.exists():
            self.metrics.register_error(self.agent_id, f"Source file {solution.file} not found")
            return
        
        start = time.perf_counter()
        success = await self.client.submit_run(problem_id, language_id, source_path)
        latency = (time.perf_counter() - start) * 1000
        
        if success:
            self.metrics.register_submission(self.agent_id, problem_name, solution.language, latency)
        else:
            self.metrics.register_error(self.agent_id, f"Submission failed for {problem_name}")
