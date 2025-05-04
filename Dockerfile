FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy the project files
COPY . .

# Install dependencies using uv
RUN uv pip install -e .

# Expose the port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "quicksync.src.main:app", "--host", "0.0.0.0", "--port", "8000"]