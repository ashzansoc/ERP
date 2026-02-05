#!/bin/bash

# PostgreSQL Database Setup for ERPNext
# This script creates the required database for Frappe/ERPNext

set -e

echo "🗄️  Setting up PostgreSQL database for ERPNext..."

# Database connection details
DB_HOST="dpg-d5uif1chg0os73au5pkg-a"
DB_PORT="5432"
DB_USER="postgres"  # Change this to your actual username
DB_PASSWORD=""      # You'll be prompted for password
DB_NAME="frappe"

echo "📋 Database Configuration:"
echo "   Host: $DB_HOST"
echo "   Port: $DB_PORT"
echo "   Database: $DB_NAME"
echo ""

# Check if we can connect
echo "🔌 Testing connection to PostgreSQL server..."
if ! PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "SELECT version();" > /dev/null 2>&1; then
    echo "❌ Cannot connect to PostgreSQL server."
    echo "Please check your credentials and network connectivity."
    echo ""
    echo "Try connecting manually with:"
    echo "psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres"
    exit 1
fi

echo "✅ Connection successful!"

# Create database
echo "📦 Creating database '$DB_NAME'..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres << EOF
-- Drop database if exists (optional, comment out if you want to keep existing data)
-- DROP DATABASE IF EXISTS $DB_NAME;

-- Create database
CREATE DATABASE $DB_NAME;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Connect to the new database and create extensions
\c $DB_NAME

-- Create required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

EOF

echo "✅ Database '$DB_NAME' created successfully!"
echo ""
echo "🔧 Next steps:"
echo "1. Update your ERPNext configuration with these database details"
echo "2. Run the ERPNext site creation command"
