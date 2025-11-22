#!/bin/bash
# Secure Database Schema Setup for SLMBench
# This script prompts for your database password securely and loads the schema

set -e  # Exit on error

echo "========================================="
echo "SLMBench Database Schema Setup"
echo "========================================="
echo ""
echo "This script will:"
echo "  1. Securely prompt for your database password"
echo "  2. Load the schema into the 'slmbench' database"
echo "  3. Verify the tables were created"
echo ""

# Database connection details
DB_HOST="slmbench-prod-do-user-29377895-0.h.db.ondigitalocean.com"
DB_PORT="25060"
DB_USER="doadmin"
DB_NAME="slmbench"

# Prompt for password securely (input hidden)
echo -n "Enter database password: "
read -s DB_PASSWORD
echo ""
echo ""

# Construct connection string
CONNECTION_STRING="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=require"

echo "========================================="
echo "Step 1: Loading schema..."
echo "========================================="

# Load schema
if psql "$CONNECTION_STRING" < database/schema.sql 2>&1; then
    echo "✅ Schema loaded successfully!"
else
    echo "❌ Error loading schema"
    exit 1
fi

echo ""
echo "========================================="
echo "Step 2: Verifying tables..."
echo "========================================="

# Verify tables
psql "$CONNECTION_STRING" -c "\dt"

echo ""
echo "========================================="
echo "✅ Database setup complete!"
echo "========================================="
echo ""
echo "Created tables:"
echo "  - evaluation_orders"
echo "  - enterprise_subscriptions"
echo ""
echo "You can now proceed to Phase 2: Stripe configuration"
echo ""

# Clear password from memory
unset DB_PASSWORD
unset CONNECTION_STRING
