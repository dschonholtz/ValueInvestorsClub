#!/usr/bin/env python3
"""
Custom server script to run the API on a specific port
"""
import uvicorn
import sys
import os

# Add the project root to the path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the application from main.py
from api.main import app

if __name__ == "__main__":
    PORT = 8000  # Use standard port for frontend compatibility
    print(f"Starting server on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)