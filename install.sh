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

# Create virtual environment if it doesn't exist
echo "🔨 Setting up Python environment..."
if [ ! -d ".venv" ]; then
    echo "📝 Creating virtual environment..."
    uv venv .venv
    echo "✅ Virtual environment created at .venv/"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies using requirements files
echo "📥 Installing dependencies..."

# Install production dependencies
echo "⚙️ Installing production dependencies..."
uv pip install -r requirements.txt

# Check if we're in a development environment
if [ -z "${PRODUCTION_ENV:-}" ]; then
    echo "🧪 Installing development and test dependencies..."
    uv pip install -r test-requirements.txt
    
    if [ -f "requirements-dev.txt" ]; then
        echo "🔧 Installing additional development tools..."
        uv pip install -r requirements-dev.txt
    fi
else
    echo "🏭 Production environment detected, skipping dev dependencies"
fi

echo "✨ Installation complete! Virtual environment is active."
echo "👉 To deactivate the virtual environment when finished, run: deactivate"