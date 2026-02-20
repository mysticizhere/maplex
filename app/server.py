import sys
from pathlib import Path

# Ensure project root is on path when this file is loaded by path (e.g. fastmcp dev inspector app/server.py)
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from fastmcp import FastMCP

from app.service_clients.ogc_client.ogc_client import OgcApiClient


mcp = FastMCP("ogc-mcp-backend")


@mcp.tool(name="test")
async def llm_stream(data: dict) -> dict:
    """Call OGC example with the given data. Pass a dict (e.g. {"key": "value"}) as input."""
    result = await OgcApiClient.example(data)
    return result

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port="3001")

