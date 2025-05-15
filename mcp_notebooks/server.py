from mcp_notebooks.app.api import mcp

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=3001,
        log_level="debug",
    )
