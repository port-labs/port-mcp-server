#!/bin/sh

# Cross-platform entrypoint script for Port MCP Server
# Supports both Linux and Windows containers

# Function to activate virtual environment
activate_venv() {
    # Check for Unix-style virtual environment first
    if [ -f ".venv/bin/activate" ]; then
        . .venv/bin/activate
        echo "Activated virtual environment (Unix-style)"
    elif [ -f ".venv/Scripts/activate" ]; then
        # Windows-style virtual environment
        . .venv/Scripts/activate
        echo "Activated virtual environment (Windows-style)"
    else
        echo "Warning: Virtual environment not found, continuing without activation"
    fi
}

# Function to ensure log file exists
ensure_log_file() {
    # Use PORT_LOG_PATH if set, otherwise default to /tmp/port-mcp.log
    LOG_FILE="${PORT_LOG_PATH:-/tmp/port-mcp.log}"
    
    # Create log directory if it doesn't exist
    LOG_DIR=$(dirname "$LOG_FILE")
    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR" 2>/dev/null || true
    fi
    
    # Touch the log file if possible
    touch "$LOG_FILE" 2>/dev/null || echo "Warning: Could not create log file at $LOG_FILE"
}

# Main execution
echo "Starting Port MCP Server..."

# Activate virtual environment
activate_venv

# Ensure log file exists
ensure_log_file

# Use environment variables with better fallback handling
REGION="${PORT_REGION:-${REGION:-EU}}"
LOG_LEVEL="${PORT_LOG_LEVEL:-${LOG_LEVEL:-ERROR}}"
API_VALIDATION="${PORT_API_VALIDATION_ENABLED:-${API_VALIDATION_ENABLED:-False}}"

# Build command arguments
if [ -n "$PORT_CLIENT_ID" ] && [ -n "$PORT_CLIENT_SECRET" ]; then
    echo "Using environment variables for authentication"
    exec python -m src \
        --client-id "$PORT_CLIENT_ID" \
        --client-secret "$PORT_CLIENT_SECRET" \
        --region "$REGION" \
        --log-level "$LOG_LEVEL" \
        --api-validation-enabled "$API_VALIDATION" \
        "$@"
else
    echo "No authentication environment variables found, passing all arguments to server"
    exec python -m src "$@"
fi