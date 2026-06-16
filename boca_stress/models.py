from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import yaml
from pathlib import Path

class SolutionModel(BaseModel):
    file: str
    language: str
    weight: float = 1.0

class ProblemModel(BaseModel):
    weight: float = 1.0
    solutions: List[SolutionModel]

class SolutionsConfig(BaseModel):
    problems: Dict[str, ProblemModel]

    @classmethod
    def load(cls, path: Path) -> "SolutionsConfig":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

class CompetitionConfig(BaseModel):
    url: str
    admin_user: str
    admin_pass: str
    problems_dir: Path
    teams_count: int

class SSHConfig(BaseModel):
    host: str
    user: str
    password: str

class DockerConfig(BaseModel):
    containers: List[str]

class DBConfig(BaseModel):
    host: str
    user: str
    password: str

class SimulationConfig(BaseModel):
    url: str
    teams_count: int
    max_think_secs: int
    solutions_dir: Path
    status_prob: float
    simulation_time_mins: int
    seed: Optional[int] = None
    ssh_configs: List[SSHConfig] = Field(default_factory=list)
    docker_configs: List[DockerConfig] = Field(default_factory=list)
    db_config: Optional[DBConfig] = None
