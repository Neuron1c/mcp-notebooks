from mcp_notebooks.app.api import mcp

if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()
    mcp.run("sse")
