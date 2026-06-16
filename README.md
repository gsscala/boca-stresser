# BOCA Stress

`boca-stress` is a CLI tool for controlled load testing on a BOCA Online Judge installation.
It simulates multiple teams submitting solutions and checking status in real-time, providing high-fidelity metrics and live infrastructure monitoring.

## Features

- **Automated Setup:** Registers problems (.zip) and creates teams automatically using BOCA's admin protocols.
- **Asynchronous Simulation:** Simulates hundreds of concurrent teams using a high-performance `asyncio` engine.
- **Infrastructure Monitoring:** Collects real-time metrics from the BOCA server via SSH, Docker, and PostgreSQL.
- **Fuzzy Matching:** Automatically maps your local problem names and languages to BOCA's internal IDs (e.g., "A" matches "1 - A - Problem Name").
- **Reproducible Tests:** Integrated random seeding for deterministic and comparable simulation runs.
- **Live TUI:** Beautiful, real-time dashboard built with `Rich` for monitoring throughput and latencies.

## Installation

```bash
# Recommended: Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package
pip install .
```

Requires Python 3.12+.

## Usage

### 1. Setup a Competition

Prepare the BOCA server with problems and teams. This command handles authentication, site discovery, and sequential problem numbering.

```bash
boca-stress setup \
  --url https://your-boca-url/boca \
  --admin-user admin \
  --admin-pass boca \
  --problems-dir ./problems \
  --teams 50
```

### 2. Run Simulation

Start the stress test. The tool will simulate team behavior (think time, status checks vs. submissions).

```bash
boca-stress run \
  --url https://your-boca-url/boca \
  --teams 80 \
  --max-think-secs 90 \
  --solutions-dir ./solutions \
  --status-prob 0.25 \
  --simulation-time-mins 120
```

### 3. Advanced Infrastructure Monitoring

Monitor the server's health (CPU, Memory, Judge Queue) during the simulation:

```bash
boca-stress run \
  --url https://your-boca-url/boca \
  --teams 100 \
  --ssh-host 192.168.1.10 --ssh-user admin --ssh-pass secret \
  --docker-container boca-web --docker-container boca-judge \
  --db-host 192.168.1.10 --db-user bocauser --db-pass bocapass
```

## Solution Directory Structure

The `solutions/` directory must contain a `solutions.yml` and the solution source files:

```text
solutions/
├── A/
│   ├── accepted.cpp
│   └── tle.py
├── B/
│   └── main.py
└── solutions.yml
```

### Example `solutions.yml`

You can assign weights to problems and specific solutions to create more realistic load profiles (e.g., more teams working on problem A than B).

```yaml
problems:
  A:
    weight: 3
    solutions:
      - file: A/accepted.cpp
        language: C++
        weight: 5
      - file: A/tle.py
        language: Python
        weight: 1
  B:
    weight: 1
    solutions:
      - file: B/main.py
        language: Python
        weight: 1
```

## Troubleshooting

### Large Problem Uploads Failing
If you see "Violation (file upload problem.)" or "Mandatory fields are empty" during setup, your BOCA server's PHP configuration is likely blocking large files.

**Fix:** Edit `php.ini` (usually in `/etc/php/8.x/apache2/php.ini`) and increase:
- `upload_max_filesize = 100M`
- `post_max_size = 100M`
- `max_execution_time = 300`

Then restart your web server (`sudo systemctl restart apache2`).

### Login Failed
Ensure you can access `https://your-url/boca/index.php?getsessionid=1` in your browser. If that works but the tool fails, check for firewall rules or IP-based restrictions.

## Development

Run tests, linting, and type-checking:

```bash
pytest
ruff check .
mypy boca_stress
```
