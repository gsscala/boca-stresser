from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box
from rich.console import Console
from rich.text import Text
from rich.progress import BarColumn, Progress, TextColumn
from datetime import datetime
import time
import asyncio
from .metrics.collector import MetricsCollector

class TUI:
    def __init__(self, metrics: MetricsCollector, simulation_time_mins: int, teams_count: int) -> None:
        self.metrics = metrics
        self.simulation_time_mins = simulation_time_mins
        self.teams_count = teams_count
        self.console = Console()

    def make_layout(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=10),
        )
        layout["main"].split_row(
            Layout(name="stats"),
            Layout(name="system", size=50),
        )
        return layout

    def get_header(self) -> Panel:
        return Panel(
            Text("BOCA Stress Test", justify="center", style="bold magenta"),
            box=box.ROUNDED
        )

    def get_stats_panel(self) -> Panel:
        elapsed_sec = time.time() - self.metrics.start_time
        total_sec = self.simulation_time_mins * 60
        remaining_sec = max(0, total_sec - elapsed_sec)
        
        table = Table.grid(expand=True)
        table.add_column(style="cyan")
        table.add_column(justify="right")
        
        table.add_row("Tempo Decorrido:", f"{int(elapsed_sec // 60):02d}:{int(elapsed_sec % 60):02d}")
        table.add_row("Tempo Restante:", f"{int(remaining_sec // 60):02d}:{int(remaining_sec % 60):02d}")
        table.add_row("Times Simuados:", str(self.teams_count))
        table.add_row("Submissões:", str(self.metrics.total_submissions))
        table.add_row("Consultas Status:", str(self.metrics.total_status_views))
        table.add_row("Erros:", f"[red]{self.metrics.total_errors}[/red]")
        table.add_row("Throughput:", f"{self.metrics.submissions_per_min:.2f} sub/min")
        table.add_row("p50 Latency (Sub):", f"{self.metrics.p50_submission_latency:.0f} ms")
        table.add_row("p90 Latency (Sub):", f"{self.metrics.p90_submission_latency:.0f} ms")
        table.add_row("p50 Judging Latency:", f"{self.metrics.p50_judging_latency/1000:.1f} s")
        
        return Panel(table, title="Estatísticas", box=box.ROUNDED)

    def _render_bar(self, value: float, color: str = "green") -> str:
        filled = int(value / 10)
        bar = "█" * filled + "░" * (10 - filled)
        return f"[{color}]{bar}[/{color}] {value:3.0f}%"

    def get_system_panel(self) -> Panel:
        sys = self.metrics.system
        table = Table.grid(expand=True)
        
        table.add_row(f"CPU:  {self._render_bar(sys.cpu, 'green')}")
        table.add_row(f"Mem:  {self._render_bar(sys.mem, 'blue')}")
        table.add_row(f"Load: {sys.load[0]:.2f} {sys.load[1]:.2f} {sys.load[2]:.2f}")
        table.add_row("")
        
        queue_val = min(100, sys.queue_size)
        table.add_row(f"Fila Autojudge: {self._render_bar(float(queue_val), 'yellow')} ({sys.queue_size})")
        
        if sys.containers:
            table.add_row("")
            table.add_row("[bold]Containers:[/bold]")
            for name, stats in sys.containers.items():
                table.add_row(f" {name[:12]:12}: CPU {stats['cpu']:3.0f}% | Mem {stats['mem']:3.0f}%")
        
        return Panel(table, title="Sistema", box=box.ROUNDED)

    def get_logs_panel(self) -> Panel:
        table = Table.grid(expand=True)
        for log in list(self.metrics.logs)[-8:]:
            ts = datetime.fromtimestamp(log.timestamp).strftime("%H:%M:%S")
            color = "white"
            if log.action == "error":
                color = "red"
            elif log.action == "submit":
                color = "green"
            elif log.action == "status":
                color = "blue"
            
            table.add_row(
                f"[{color}]{ts} Time {log.agent_id:03d}: {log.details}[/{color}]"
            )
        return Panel(table, title="Últimas Ações", box=box.ROUNDED)

    async def run(self, stop_event: asyncio.Event) -> None:
        layout = self.make_layout()
        with Live(layout, console=self.console, refresh_per_second=4, screen=True):
            while not stop_event.is_set():
                layout["header"].update(self.get_header())
                layout["stats"].update(self.get_stats_panel())
                layout["system"].update(self.get_system_panel())
                layout["footer"].update(self.get_logs_panel())
                await asyncio.sleep(0.25)
