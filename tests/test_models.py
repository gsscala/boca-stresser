import yaml
from boca_stress.models import SolutionsConfig

def test_solutions_config_load(tmp_path):
    d = tmp_path / "solutions"
    d.mkdir()
    yml = d / "solutions.yml"
    
    config_data = {
        "problems": {
            "A": {
                "weight": 3,
                "solutions": [
                    {"file": "A/accepted.cpp", "language": "C++", "weight": 5},
                    {"file": "A/tle.py", "language": "Python", "weight": 1}
                ]
            }
        }
    }
    
    with open(yml, "w") as f:
        yaml.dump(config_data, f)
    
    config = SolutionsConfig.load(yml)
    assert "A" in config.problems
    assert config.problems["A"].weight == 3
    assert len(config.problems["A"].solutions) == 2
    assert config.problems["A"].solutions[0].language == "C++"
