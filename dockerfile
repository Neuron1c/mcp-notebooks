FROM python:3.13-slim

# Create restricted user
RUN useradd -m jupyter && \
    chmod 755 /home/jupyter

# Set working directory to app
WORKDIR /home/jupyter

# Install Poetry and copy code
RUN pip install --no-cache-dir uv
COPY . .

# Install dependencies and the package itself
RUN uv sync

# Change to restricted user **after** installing everything
RUN chmod -R 555 /home/jupyter
USER jupyter

EXPOSE 3001

ENTRYPOINT ["uv", "run", "--no-cache", "python", "-m", "mcp_notebooks.server" ]
