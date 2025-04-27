#!/bin/sh

# If environment variables are provided, use them as command line arguments
source .venv/bin/activate
if [ ! -z "$PORT_CLIENT_ID" ] && [ ! -z "$PORT_CLIENT_SECRET" ]; then
    echo "Environment variables provided, using them as command line arguments"
    exec python -m src --client-id "$PORT_CLIENT_ID" --client-secret "$PORT_CLIENT_SECRET" --region "${REGION:-EU}" --log-level "${LOG_LEVEL:-ERROR}" "$@"
else
    # Otherwise, pass all arguments to the server
    echo "No environment variables provided, using default values"
    exec python -m src "$@"
fi 