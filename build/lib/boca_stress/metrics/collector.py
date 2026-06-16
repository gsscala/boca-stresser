import time
from collections import deque
from dataclasses import dataclass
from typing import List

@dataclass
class ActionLog:
    timestamp: float
    agent_id: int
    action: str
    details: str

class MetricsCollector:
    def __init__(self) -> None:
        self.total_submissions = 0
        self.total_status_views = 0
        self.total_errors = 0
        self.submission_latencies: List[float] = []
        self.status_latencies: List[float] = []
        self.logs: deque[ActionLog] = deque(maxlen=20)
        self.start_time = time.time()
        self.errors: List[str] = []

    def register_submission(self, agent_id: int, problem: str, language: str, latency: float) -> None:
        self.total_submissions += 1
        self.submission_latencies.append(latency)
        self.logs.append(ActionLog(
            time.time(), agent_id, "submit", f"Problem {problem} in {language}"
        ))

    def register_status_view(self, agent_id: int, latency: float) -> None:
        self.total_status_views += 1
        self.status_latencies.append(latency)
        self.logs.append(ActionLog(
            time.time(), agent_id, "status", "Viewed status"
        ))

    def register_error(self, agent_id: int, error: str) -> None:
        self.total_errors += 1
        self.errors.append(f"Agent {agent_id}: {error}")
        self.logs.append(ActionLog(
            time.time(), agent_id, "error", error
        ))

    @property
    def submissions_per_min(self) -> float:
        elapsed = (time.time() - self.start_time) / 60
        return self.total_submissions / elapsed if elapsed > 0 else 0

    @property
    def avg_submission_latency(self) -> float:
        return sum(self.submission_latencies) / len(self.submission_latencies) if self.submission_latencies else 0

    @property
    def avg_status_latency(self) -> float:
        return sum(self.status_latencies) / len(self.status_latencies) if self.status_latencies else 0
