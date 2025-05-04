FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY README.md .
COPY quicksync ./quicksync

RUN uv pip install .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

CMD uvicorn quicksync.src.main:app --host 0.0.0.0 --port ${PORT:-8000}