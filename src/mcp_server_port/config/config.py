import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists, but don't override existing env vars
load_dotenv(override=False)

# Port.io API configuration
PORT_API_BASE = "https://api.getport.io/v1"

# Environment variables for credentials
PORT_CLIENT_ID = os.environ.get("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.environ.get("PORT_CLIENT_SECRET") 