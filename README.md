# Maplex – OGC MCP Backend

MCP server exposing OGC API - Processes 1.0 tools (list processes, get process, execute, job status/results). Designed to work with OGC/pygeoapi deployments.

## Files

- `app/server.py` – MCP server entrypoint; registers OGC process tools.
- `app/tools/ogc/process.py` – Tools: `ogc_list_processes`, `ogc_get_process_info`, `ogc_execute_process`, `ogc_get_job_status_or_results`.
- `app/service_clients/ogc_client/ogc_client.py` – HTTP client for `/processes`, `/processes/{id}/execution`, `/jobs/{id}`, `/jobs/{id}/results`.
- `config_template.json` – Template for `config.json` (OGC `HOST`, `TIMEOUT`, `AUTH_TOKEN`, etc.).
- `requirements.txt` – Python dependencies.

## Local setup

```bash
pip install -r requirements.txt
cp config_template.json config.json
# Edit config.json: set OGC.HOST and AUTH_TOKEN
```

Run the server (streamable-http):

```bash
python -m app.server
```

Optional env: `MCP_HOST` (default `0.0.0.0`), `MCP_PORT` (default `3001`), `CONFIG_PATH` (path to config JSON).

**MCP Inspector (local dev)**  
Run from the project root and set `PYTHONPATH` so the `app` package resolves:

- PowerShell: `$env:PYTHONPATH = (Get-Location).Path; fastmcp dev inspector app/server.py`
- Bash: `PYTHONPATH=. fastmcp dev inspector app/server.py`

## Docker deployment

Build and run:

```bash
docker build -t maplex .
docker run -p 3001:3001 -v "$(pwd)/config.json:/app/config.json:ro" maplex
```

Or with Docker Compose:

```bash
# Create config first (copy from config_template.json, set OGC.HOST and AUTH_TOKEN)
docker compose up -d
```

In `docker-compose.yml`, uncomment the `volumes` section to mount your `config.json`. Override port with `MCP_PORT=8080` in the environment or in `.env`.

**Env vars in container**

| Variable       | Default        | Description                    |
|----------------|----------------|--------------------------------|
| `MCP_HOST`     | `0.0.0.0`      | Bind address                   |
| `MCP_PORT`     | `3001`         | Server port                    |
| `CONFIG_PATH`  | `/app/config.json` | Path to config JSON (or mount) |

The image includes a default config from `config_template.json`; for production, mount a real `config.json` with your OGC URL and `AUTH_TOKEN`.

