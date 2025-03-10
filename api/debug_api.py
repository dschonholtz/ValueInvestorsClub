#!/usr/bin/env python3
"""
Debug script to test API endpoints directly
"""

import requests  # type: ignore  # Missing stubs for requests library
import json
import sys
from typing import Dict, Any, Optional
BASE_URL = "http://localhost:"
# Check if a port is provided as command line argument
if len(sys.argv) > 1:
    BASE_URL += sys.argv[1]
else:
    BASE_URL += "8000"

def pretty_print_json(data: Dict[str, Any]) -> None:
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def check_endpoint(endpoint: str, params: Optional[Dict[str, Any]] = None) -> None:
    """Check if an endpoint is working correctly"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n==== Testing {url} ====")
    
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Response (truncated):")
            data = response.json()
            
            if isinstance(data, list):
                print(f"Received {len(data)} items")
                if len(data) > 0:
                    print("First item:")
                    pretty_print_json(data[0])
            else:
                pretty_print_json(data)
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def main():
    """Main function"""
    # Check health endpoint
    check_endpoint("/health")
    
    # Check ideas endpoint
    check_endpoint("/ideas/", {"limit": 1})
    
    # Check companies endpoint
    check_endpoint("/companies/", {"limit": 1})
    
    # Check users endpoint
    check_endpoint("/users/", {"limit": 1})
    
    # If an idea ID is available, check idea detail endpoint
    response = requests.get(f"{BASE_URL}/ideas/", {"limit": 1})
    if response.status_code == 200 and len(response.json()) > 0:
        idea_id = response.json()[0]["id"]
        check_endpoint(f"/ideas/{idea_id}")
        check_endpoint(f"/ideas/{idea_id}/performance")

if __name__ == "__main__":
    main()