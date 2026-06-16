import asyncio
import random
from typing import List
from .agents import TeamAgent
from .boca.team import BocaTeam
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
            self.collectors.append(SSHCollector(ssh.host, ssh.user, ssh.password, ssh.db_container))
        for docker in config.docker_configs:
            self.collectors.append(DockerCollector(docker.containers))
        if config.db_config:
            self.collectors.append(PostgresCollector(config.db_config.host, config.db_config.user, config.db_config.password))

    async def run(self) -> None:
        if self.config.seed is not None:
            random.seed(self.config.seed)

        # Fetch problems and languages once to reduce load
        shared_problem_ids = {}
        shared_language_ids = {}
        
        async with BocaTeam(self.config.url) as client:
            # Use team001 as a bootstrap to get metadata
            if await client.login("team001", "team001"):
                shared_problem_ids = await client.get_problems()
                shared_language_ids = await client.get_languages()

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
            # Inject shared metadata
            agent.problem_ids = shared_problem_ids
            agent.language_ids = shared_language_ids
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
            self.print_summary()

    def print_summary(self) -> None:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich import box
        import time

        console = Console()
        elapsed_sec = time.time() - self.metrics.start_time
        
        table = Table(title="Resumo da Simulação", box=box.ROUNDED, expand=True)
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", justify="right", style="green")

        table.add_row("Duração Total", f"{int(elapsed_sec // 60):02d}:{int(elapsed_sec % 60):02d}")
        table.add_row("Total de Times", str(self.config.teams_count))
        table.add_row("Submissões Realizadas", str(self.metrics.total_submissions))
        table.add_row("Consultas de Status", str(self.metrics.total_status_views))
        table.add_row("Total de Erros", f"[red]{self.metrics.total_errors}[/red]")
        table.add_row("Throughput Médio", f"{self.metrics.submissions_per_min:.2f} sub/min")
        
        table.add_section()
        table.add_row("p50 Latência Submissão", f"{self.metrics.p50_submission_latency:.0f} ms")
        table.add_row("p90 Latência Submissão", f"{self.metrics.p90_submission_latency:.0f} ms")
        table.add_row("p50 Latência Julgamento", f"{self.metrics.p50_judging_latency/1000:.1f} s")
        
        if self.metrics.system.cpu > 0:
            table.add_section()
            table.add_row("CPU Final (Host)", f"{self.metrics.system.cpu:.1f}%")
            table.add_row("Memória Final (Host)", f"{self.metrics.system.mem:.1f}%")
            table.add_row("Fila Autojudge Final", str(self.metrics.system.queue_size))

        console.print("\n")
        console.print(Panel(table, border_style="bold blue"))
        
        if self.metrics.errors:
            error_table = Table(title="Últimos Erros Detalhados", box=box.SIMPLE, expand=True)
            error_table.add_column("Agent", style="yellow", width=10)
            error_table.add_column("Mensagem de Erro", style="red")
            
            # Show last 10 unique errors
            seen_errors = set()
            count = 0
            for err in reversed(self.metrics.errors):
                if err not in seen_errors:
                    parts = err.split(": ", 1)
                    agent = parts[0] if len(parts) > 1 else "Unknown"
                    msg = parts[1] if len(parts) > 1 else err
                    error_table.add_row(agent, msg)
                    seen_errors.add(err)
                    count += 1
                if count >= 10:
                    break
            
            if count > 0:
                console.print(error_table)
        
        console.print("\n[bold blue]Benchmark finalizado.[/bold blue]")

    async def run_collector(self, collector: RemoteCollector) -> None:
        while not self.stop_event.is_set():
            try:
                data = await collector.collect()
                if data:
                    self.metrics.update_system_metrics(data)
            except Exception:
                pass
            await asyncio.sleep(5)
        
        # Cleanup
        if hasattr(collector, "close"):
            await collector.close()
