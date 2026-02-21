from fastmcp import FastMCP

from app.tools.ogc.process import register_tools
from app.utils import CONFIG


mcp = FastMCP("ogc-mcp-backend")
register_tools(mcp)

if __name__ == "__main__":
    host = CONFIG.config.get("HOST", "0.0.0.0")
    port = CONFIG.config.get("PORT", 3001)
    mcp.run(transport="streamable-http", host=host, port=port)

