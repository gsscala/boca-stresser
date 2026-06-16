import time
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ActionLog:
    timestamp: float
    agent_id: int
    action: str
    details: str

@dataclass
class SystemMetrics:
    cpu: float = 0.0
    mem: float = 0.0
    load: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    queue_size: int = 0
    containers: Dict[str, Dict[str, float]] = field(default_factory=dict)

class MetricsCollector:
    def __init__(self) -> None:
        self.total_submissions = 0
        self.total_status_views = 0
        self.total_errors = 0
        self.submission_latencies: List[float] = []
        self.status_latencies: List[float] = []
        self.judging_latencies: List[float] = []
        self.logs: deque[ActionLog] = deque(maxlen=20)
        self.start_time = time.time()
        self.errors: List[str] = []
        self.system = SystemMetrics()

    def register_submission(self, agent_id: int, problem: str, language: str, latency: float) -> None:
        self.total_submissions += 1
        self.submission_latencies.append(latency)
        self.logs.append(ActionLog(
            time.time(), agent_id, "submit", f"Problem {problem} in {language}"
        ))

    def register_judging_latency(self, agent_id: int, latency_ms: float) -> None:
        self.judging_latencies.append(latency_ms)

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

    def update_system_metrics(self, data: Dict[str, Any]) -> None:
        if "cpu" in data:
            self.system.cpu = data["cpu"]
        if "mem" in data:
            self.system.mem = data["mem"]
        if "load" in data:
            self.system.load = data["load"]
        if "queue_size" in data:
            self.system.queue_size = data["queue_size"]
        if "containers" in data:
            self.system.containers.update(data["containers"])

    @property
    def submissions_per_min(self) -> float:
        elapsed = (time.time() - self.start_time) / 60
        return self.total_submissions / elapsed if elapsed > 0 else 0

    @property
    def avg_submission_latency(self) -> float:
        return sum(self.submission_latencies) / len(self.submission_latencies) if self.submission_latencies else 0

    def _get_percentile(self, data: List[float], p: float) -> float:
        if not data:
            return 0
        sorted_data = sorted(data)
        idx = int(len(sorted_data) * p / 100)
        return sorted_data[min(idx, len(sorted_data) - 1)]

    @property
    def p50_submission_latency(self) -> float:
        return self._get_percentile(self.submission_latencies, 50)

    @property
    def p90_submission_latency(self) -> float:
        return self._get_percentile(self.submission_latencies, 90)

    @property
    def p50_judging_latency(self) -> float:
        return self._get_percentile(self.judging_latencies, 50)

    @property
    def avg_judging_latency(self) -> float:
        return sum(self.judging_latencies) / len(self.judging_latencies) if self.judging_latencies else 0
