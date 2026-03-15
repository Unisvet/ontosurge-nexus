FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.4 /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
# Install dependencies into the system environment to avoid activating venvs in Docker
RUN uv pip install --system -r pyproject.toml

COPY . .
# Cloud Run expects traffic on port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
