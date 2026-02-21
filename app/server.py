import sys
from pathlib import Path

# Ensure project root is on path when this file is loaded by path (e.g. fastmcp dev inspector app/server.py)
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from fastmcp import FastMCP

from app.tools.ogc.process import register_tools


mcp = FastMCP("ogc-mcp-backend")
register_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port="3001")

