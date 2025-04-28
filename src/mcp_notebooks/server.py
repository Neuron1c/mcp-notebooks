from mcp_notebooks.app.api import mcp
import dotenv

if __name__ == "__main__":
    dotenv.load_dotenv()
    mcp.run("sse")
