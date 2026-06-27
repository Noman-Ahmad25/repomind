#Use a lightweight python base image
FROM python:3.12-slim-bookworm AS builder

# Install uv for fast, reliable dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy configuration files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Final runtime stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install git since RepoMind clones repositories dynamically
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment and application code from the builder stage
COPY --from=builder /app/.venv /app/.venv
COPY . /app

# Place the virtual environment's executables into the system PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set the entrypoint to the repomind executable or module call
ENTRYPOINT ["python", "-m", "repomind.main"]