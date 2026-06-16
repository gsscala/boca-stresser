from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box
from rich.console import Console
from rich.text import Text
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
            Layout(name="system", size=40),
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
        table.add_row("p50 Latency (Sub):", f"{self.metrics.avg_submission_latency:.0f} ms")
        
        return Panel(table, title="Estatísticas", box=box.ROUNDED)

    def get_system_panel(self) -> Panel:
        # Placeholder for system metrics
        table = Table.grid(expand=True)
        table.add_row("CPU:  [green]████████░░░░░░░[/green] 53%")
        table.add_row("Mem:  [blue]██████░░░░░░░░░[/blue] 40%")
        table.add_row("Load: 1.25 1.10 0.95")
        table.add_row("")
        table.add_row("Fila Autojudge: [yellow]████░░░░░░░░░░░[/yellow] 12")
        
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
