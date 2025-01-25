#!/bin/bash

# Get password if provided as argument
DB_PASS=${1:-"postgres"}  # Default to "postgres" if no password provided

# Export password for postgres commands
export PGPASSWORD="$DB_PASS"

# Add host parameter to connect to Docker container
PSQL_OPTS="-h localhost -U postgres"

echo "=== Database Schema Information for 'ideas' ==="
echo "\nDetailed information about all tables and their columns:"

# Query to get detailed information about all columns in all tables
psql $PSQL_OPTS -d ideas << EOF
SELECT 
    t.table_name,
    c.column_name,
    c.data_type,
    c.character_maximum_length,
    c.column_default,
    c.is_nullable,
    c.numeric_precision,
    c.numeric_scale,
    pg_catalog.col_description(format('%s.%s',t.table_schema,t.table_name)::regclass::oid, c.ordinal_position) as column_description
FROM 
    information_schema.tables t
    JOIN information_schema.columns c ON t.table_name = c.table_name
WHERE 
    t.table_schema = 'public'
ORDER BY 
    t.table_name,
    c.ordinal_position;
EOF

echo "\n=== Table Sizes and Row Counts ==="
psql $PSQL_OPTS -d ideas << EOF
SELECT
    relname as table_name,
    n_live_tup as row_count,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size
FROM
    pg_stat_user_tables
ORDER BY
    n_live_tup DESC;
EOF

echo "\n=== Foreign Key Relationships ==="
psql $PSQL_OPTS -d ideas << EOF
SELECT
    tc.table_name as table_name,
    kcu.column_name as column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM
    information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
WHERE
    tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
ORDER BY
    tc.table_name;
EOF

# Clean up
unset PGPASSWORD 