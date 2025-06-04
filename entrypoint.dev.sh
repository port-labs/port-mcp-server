#!/bin/bash

# Development entrypoint script

# Activate Poetry virtual environment
source .venv/bin/activate

# Create log file for debugging
touch /tmp/port-mcp-dev.log

# Function to run the MCP server
run_server() {
    if [ ! -z "$PORT_CLIENT_ID" ] && [ ! -z "$PORT_CLIENT_SECRET" ]; then
        echo "Starting MCP server with provided credentials..."
        exec poetry run python -m src \
            --client-id "$PORT_CLIENT_ID" \
            --client-secret "$PORT_CLIENT_SECRET" \
            --region "${PORT_REGION:-EU}" \
            --log-level "${PORT_LOG_LEVEL:-DEBUG}" \
            --api-validation-enabled "${PORT_API_VALIDATION_ENABLED:-False}" \
            "$@"
    else
        echo "Starting MCP server - credentials will be provided via Cursor..."
        exec poetry run python -m src "$@"
    fi
}

# Always run the server in development mode
# Auto-reload will be handled by Cursor reconnecting when files change
echo "Starting MCP server in development mode..."
run_server "$@" 