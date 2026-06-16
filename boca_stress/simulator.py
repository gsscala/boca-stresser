import asyncio
import random
from typing import List
from .agents import TeamAgent
from .metrics.collector import MetricsCollector
from .tui import TUI
from .models import SolutionsConfig, SimulationConfig
from .metrics.ssh import SSHCollector, RemoteCollector
from .metrics.postgres import PostgresCollector
from .metrics.docker import DockerCollector

class Simulator:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.metrics = MetricsCollector()
        self.stop_event = asyncio.Event()
        self.solutions_config = SolutionsConfig.load(config.solutions_dir / "solutions.yml")
        
        self.collectors: List[RemoteCollector] = []
        for ssh in config.ssh_configs:
            self.collectors.append(SSHCollector(ssh.host, ssh.user, ssh.password))
        for docker in config.docker_configs:
            self.collectors.append(DockerCollector(docker.containers))
        if config.db_config:
            self.collectors.append(PostgresCollector(config.db_config.host, config.db_config.user, config.db_config.password))

    async def run(self) -> None:
        if self.config.seed is not None:
            random.seed(self.config.seed)

        agents = []
        for i in range(1, self.config.teams_count + 1):
            name = f"team{i:03d}"
            agent = TeamAgent(
                agent_id=i,
                url=self.config.url,
                username=name,
                password=name,
                config=self.solutions_config,
                solutions_dir=self.config.solutions_dir,
                status_prob=self.config.status_prob,
                max_think_secs=self.config.max_think_secs,
                metrics_collector=self.metrics
            )
            agents.append(agent)

        tui = TUI(self.metrics, self.config.simulation_time_mins, self.config.teams_count)
        
        # Start agents
        agent_tasks = [asyncio.create_task(a.run(self.stop_event)) for a in agents]
        
        # Start collectors
        collector_tasks = [asyncio.create_task(self.run_collector(c)) for c in self.collectors]
        
        # Start TUI
        tui_task = asyncio.create_task(tui.run(self.stop_event))

        try:
            # Wait for simulation time
            await asyncio.sleep(self.config.simulation_time_mins * 60)
        except asyncio.CancelledError:
            pass
        finally:
            self.stop_event.set()
            await asyncio.gather(*agent_tasks, *collector_tasks, return_exceptions=True)
            await tui_task

    async def run_collector(self, collector: RemoteCollector) -> None:
        while not self.stop_event.is_set():
            try:
                await collector.collect()
                # TODO: Integrate collector data with metrics and TUI
            except Exception:
                pass
            await asyncio.sleep(5)
