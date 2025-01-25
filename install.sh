#!/usr/bin/env bash

set -euo pipefail

echo "🔍 Checking for uv installation..."

if ! command -v uv &> /dev/null; then
    echo "📦 uv not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add uv to the current PATH
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "✅ uv is already installed"
fi

# Initialize the project only if pyproject.toml doesn't exist
echo "🔨 Checking project initialization..."
if [ ! -f "pyproject.toml" ]; then
    echo "📝 Initializing new project..."
    uv init .
else
    echo "✅ Project already initialized"
fi

# Install dependencies using uv add
echo "📥 Installing dependencies..."
# API dependencies
uv add "fastapi>=0.109.0" "uvicorn>=0.27.0" "sqlalchemy>=2.0.0" "psycopg>=3.2.3" "pydantic>=2.0.0"

# Scraper dependencies
uv add selenium pandas

echo "✨ Installation complete!" 