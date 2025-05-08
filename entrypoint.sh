#!/bin/sh

# If environment variables are provided, use them as command line arguments
source .venv/bin/activate
touch /tmp/port-mcp.log
if [ ! -z "$PORT_CLIENT_ID" ] && [ ! -z "$PORT_CLIENT_SECRET" ]; then
    exec python -m src --client-id "$PORT_CLIENT_ID" --client-secret "$PORT_CLIENT_SECRET" --region "${REGION:-EU}" --log-level "${LOG_LEVEL:-ERROR}" --api-validation-enabled "${API_VALIDATION_ENABLED:-False}" "$@"
else
    # Otherwise, pass all arguments to the server
    exec python -m src "$@"
fi 