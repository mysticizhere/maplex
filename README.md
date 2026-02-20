# OGC MCP Backend Boilerplate

This is a minimal MCP backend service that talks to OGC APIs (for example those described at `https://ogcapi.ogc.org/`) and is designed to work cleanly with pygeoapi-based deployments.

## Files

- `requirements.txt` – Python dependencies (`httpx`, `pygeoapi`, `fastmcp`).
- `ogc_client.py` – small HTTP client for OGC API Features, Records, and EDR.
- `mcp_server.py` – MCP server exposing modular tools that wrap the OGC client.
- `ogc_mcp_schema.json` – JSON Schema describing modular mappings from OGC API components to MCP tools.

## Setup

```bash
pip install -r requirements.txt
```

Set the base URL of your target OGC API (often a pygeoapi instance):

```bash
set OGC_BASE_URL=https://your-pygeoapi.example.org/ogcapi
```

## Running the MCP server

The server is designed to run over stdio as an MCP backend. For simple local testing you can run:

```bash
python mcp_server.py
```

Integrate `mcp_server.py` into your MCP host according to that host's configuration format, wiring the exposed tools (e.g. `list_feature_collections`, `get_features`, `search_records`, `edr_position`) as needed.

