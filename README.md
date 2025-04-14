# mcp-notebooks
Notebook execution MCP server

Pretty dangerous to use in its current state

# Rationale

Why not just execute code with literally any other already existing python execution server. This MCP server allows your LLM to progressively execute code and react to mistakes faster in a sort of EDA fashion. Variables are retained in the kernel and can be used in future executions.

# Claude install

Okay listen buddy, it's not a one line process and run some node something. This really really should be run in a docker environment to protect your system from the AI overlor... I mean Claude. So go install docker and come back

Welcome back. This is not on DockerHub yet so run the following commands:

```bash
git clone git@github.com:Neuron1c/mcp-notebooks.git
cd mcp-notebooks

docker build . -t mcp-notebooks:latest
```

Halfway there, add the following to `your claude_desktop_config.json`

## StdIO
```json
{
  "mcpServers": {
    "notebooks": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "mcp-notebooks:latest"
      ]
    }
  }
}
```

## SSE

Or run it manually

```bash
docker run -p 3001:3001 mcp-notebooks:latest
```

And now the config.json
```json
{
  "mcpServers": {
    "notebooks": {
      "command": "npx",
      "args": [
        "supergateway",
        "--sse",
        "http://localhost:3001/sse"
      ]
    }
  }
}
```
# Add Python Libraries

As it stands the project dependencies are scoped to the bare minimum of what's needed to run the server. To add more you need to install `poetry`, after you have fought with that (protip use `pipx`)

```bash
poetry add your-package
```

recommended packages to add 
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn

I've found the AI really tries to use the graphing packages when demonstrating things to your

# TODO
- kernel timeout (10 minutes? env var it)
- Sandbox the environment more
- Scheme a data ingestion scenario (Kedro catalog?)
- Dependency injection (Or just let the user pull and build their own container)
- Switch to uv?