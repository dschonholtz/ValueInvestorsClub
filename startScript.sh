#!/bin/bash

# Get password if provided as argument
DB_PASS=${1:-"postgres"}  # Default to "postgres" if no password provided

# Export password for postgres commands
export PGPASSWORD="$DB_PASS"

# Add host parameter to connect to Docker container
PSQL_OPTS="-h localhost -U postgres"

# List all databases
echo "\nListing all databases:"
psql $PSQL_OPTS -c "\l" || { echo "Failed to list databases"; exit 1; }

# Create the database in postgres (only if it doesn't exist)
psql $PSQL_OPTS -c "SELECT 1 FROM pg_database WHERE datname = 'ideas'" | grep -q 1 || \
psql $PSQL_OPTS -c "CREATE DATABASE ideas;"

# Create the tables in the database
psql $PSQL_OPTS -d ideas -f VIC_IDEAS.sql || { echo "Failed to create tables"; exit 1; }

# List all tables in the database
echo "\nListing all tables in the database:"
psql $PSQL_OPTS -d ideas -c "\dt" || { echo "Failed to list tables"; exit 1; }

# Clean up
unset PGPASSWORD
