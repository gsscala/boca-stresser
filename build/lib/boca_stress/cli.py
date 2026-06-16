import typer
from typing import Optional, List
from rich.console import Console

app = typer.Typer(help="BOCA Stress Test CLI")
console = Console()

__version__ = "0.1.0"

def version_callback(value: bool) -> None:
    if value:
        console.print(f"boca-stress version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show version and exit."
    ),
) -> None:
    pass

@app.command()
def setup(
    url: str = typer.Option(..., help="URL of BOCA installation"),
    admin_user: str = typer.Option("admin", help="Admin username"),
    admin_pass: str = typer.Option("boca", help="Admin password"),
    problems_dir: str = typer.Option("problems/", help="Directory with problem .zip files"),
    teams: int = typer.Option(50, help="Number of teams to create"),
) -> None:
    """
    Prepare a test competition by registering problems and creating teams.
    """
    import asyncio
    from .boca.admin import BocaAdmin
    from pathlib import Path

    async def _setup() -> None:
        async with BocaAdmin(url) as admin:
            admin.set_admin_pass(admin_pass)
            if not await admin.login(admin_user, admin_pass):
                console.print("[bold red]Login failed![/bold red]")
                return

            console.print("[green]Logged in as admin.[/green]")

            # Upload problems
            prob_path = Path(problems_dir)
            if prob_path.exists():
                for zip_file in prob_path.glob("*.zip"):
                    console.print(f"Uploading problem {zip_file.name}...")
                    success = await admin.upload_problem(zip_file)
                    if success:
                        console.print(f"[green]Problem {zip_file.name} uploaded.[/green]")
                    else:
                        console.print(f"[red]Failed to upload problem {zip_file.name}.[/red]")
            
            # Create teams
            console.print(f"Creating {teams} teams...")
            teams_data = ""
            for i in range(1, teams + 1):
                name = f"team{i:03d}"
                teams_data += f"[user]\nusernumber={i}\nusername={name}\nuserpassword={name}\nuserfullname=Team {i}\nusertype=team\n\n"
            
            success = await admin.import_teams(teams_data)
            if success:
                console.print(f"[green]{teams} teams created.[/green]")
            else:
                console.print("[red]Failed to create teams.[/red]")

    asyncio.run(_setup())

@app.command()
def run(
    url: str = typer.Option(..., help="URL of BOCA installation"),
    teams: int = typer.Option(80, help="Number of simulated teams"),
    max_think_secs: int = typer.Option(90, help="Maximum think time between actions"),
    solutions_dir: str = typer.Option("solutions/", help="Directory with solutions to submit"),
    status_prob: float = typer.Option(0.25, help="Probability of checking status instead of submitting"),
    simulation_time_mins: int = typer.Option(120, help="Simulation duration in minutes"),
    seed: Optional[int] = typer.Option(None, help="Random seed for reproducibility"),
    ssh_host: Optional[List[str]] = typer.Option(None, help="SSH host(s) to monitor"),
    ssh_user: Optional[str] = typer.Option(None, help="SSH username"),
    ssh_pass: Optional[str] = typer.Option(None, help="SSH password"),
    docker_container: Optional[List[str]] = typer.Option(None, help="Docker container(s) to monitor"),
    db_host: Optional[str] = typer.Option(None, help="Database host to monitor"),
    db_user: Optional[str] = typer.Option(None, help="Database username"),
    db_pass: Optional[str] = typer.Option(None, help="Database password"),
) -> None:
    """
    Execute the stress test simulation.
    """
    import asyncio
    from .simulator import Simulator
    from .models import SimulationConfig, SSHConfig, DockerConfig, DBConfig
    from pathlib import Path

    ssh_configs = []
    if ssh_host and ssh_user and ssh_pass:
        for host in ssh_host:
            ssh_configs.append(SSHConfig(host=host, user=ssh_user, password=ssh_pass))

    docker_configs = []
    if docker_container:
        docker_configs.append(DockerConfig(containers=docker_container))

    db_config = None
    if db_host and db_user and db_pass:
        db_config = DBConfig(host=db_host, user=db_user, password=db_pass)

    config = SimulationConfig(
        url=url,
        teams_count=teams,
        max_think_secs=max_think_secs,
        solutions_dir=Path(solutions_dir),
        status_prob=status_prob,
        simulation_time_mins=simulation_time_mins,
        seed=seed,
        ssh_configs=ssh_configs,
        docker_configs=docker_configs,
        db_config=db_config
    )

    sim = Simulator(config)
    try:
        asyncio.run(sim.run())
    except KeyboardInterrupt:
        console.print("[yellow]Simulation interrupted by user.[/yellow]")

if __name__ == "__main__":
    app()
