#!/usr/bin/env python3
"""
Schema validation tool to ensure API contract compatibility.

This script generates an OpenAPI schema from the FastAPI app and validates
that it matches the expected contract for frontend TypeScript types.

Run with: python -m api.validate_schema
"""
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the FastAPI app
from api.main import app

def generate_openapi_schema() -> Dict[str, Any]:
    """Generate OpenAPI schema from FastAPI app."""
    return app.openapi()

def write_schema_to_file(schema: Dict[str, Any], file_path: str) -> None:
    """Write OpenAPI schema to file."""
    with open(file_path, "w") as f:
        json.dump(schema, f, indent=2)

def validate_schema(schema: Dict[str, Any]) -> bool:
    """
    Validate the schema against known requirements.
    
    Returns True if valid, False otherwise.
    """
    # Check that essential endpoints are present
    paths = schema.get("paths", {})
    required_endpoints = [
        "/ideas/",
        "/ideas/{idea_id}",
        "/companies/",
        "/users/",
    ]
    
    missing_endpoints = []
    for endpoint in required_endpoints:
        if endpoint not in paths:
            missing_endpoints.append(endpoint)
    
    if missing_endpoints:
        print(f"Missing required endpoints: {', '.join(missing_endpoints)}")
        return False
    
    # Check that essential models/schemas are present
    components = schema.get("components", {})
    schemas = components.get("schemas", {})
    
    required_schemas = [
        "IdeaResponse",
        "IdeaDetailResponse",
        "CompanyResponse",
        "UserResponse",
        "PerformanceResponse",
    ]
    
    missing_schemas = []
    for schema_name in required_schemas:
        if schema_name not in schemas:
            missing_schemas.append(schema_name)
    
    if missing_schemas:
        print(f"Missing required schemas: {', '.join(missing_schemas)}")
        return False
    
    # Check for required fields in IdeaResponse
    idea_response = schemas.get("IdeaResponse", {})
    idea_properties = idea_response.get("properties", {})
    
    required_idea_fields = [
        "id",
        "company_id",
        "user_id",
        "date",
        "is_short",
        "is_contest_winner",
    ]
    
    missing_idea_fields = []
    for field in required_idea_fields:
        if field not in idea_properties:
            missing_idea_fields.append(field)
    
    if missing_idea_fields:
        print(f"Missing required fields in IdeaResponse: {', '.join(missing_idea_fields)}")
        return False
    
    return True

def main() -> int:
    """Main function."""
    print("Generating OpenAPI schema...")
    schema = generate_openapi_schema()
    
    # Create output directory if it doesn't exist
    output_dir = Path("api") / "schema"
    output_dir.mkdir(exist_ok=True)
    
    # Write schema to file
    schema_file = output_dir / "openapi.json"
    write_schema_to_file(schema, schema_file)
    print(f"Schema written to {schema_file}")
    
    # Validate schema
    print("Validating schema...")
    if validate_schema(schema):
        print("Schema validation successful!")
        return 0
    else:
        print("Schema validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())