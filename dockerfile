FROM python:3.13-slim

# Create restricted user
RUN useradd -m jupyter && \
    chmod 755 /home/jupyter

# Set working directory to app
WORKDIR /home/jupyter

# Install Poetry and copy code
RUN pip install --no-cache-dir poetry
COPY . .

# Install dependencies and the package itself
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Change to restricted user **after** installing everything
RUN chmod -R 555 /home/jupyter
USER jupyter

EXPOSE 3001

ENTRYPOINT ["poetry", "run", "python", "-m", "mcp_notebooks.server" ]
