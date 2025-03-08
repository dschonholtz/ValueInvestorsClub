FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including PostgreSQL libraries
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && \
    ln -sf "$HOME/.local/bin/uv" /usr/local/bin/uv

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose the application port
EXPOSE 8000

# Start the API server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]