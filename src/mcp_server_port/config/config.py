from dotenv import load_dotenv

# Load environment variables from .env file if it exists, but don't override existing env vars
load_dotenv(override=False)

# Port.io API configuration
PORT_API_BASE = "https://api.getport.io/v1"

# Default values (can be overridden by args or env vars)
PORT_CLIENT_ID = None
PORT_CLIENT_SECRET = None
REGION = "EU"
