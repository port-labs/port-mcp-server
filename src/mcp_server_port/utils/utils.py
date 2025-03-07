import logging
import sys

class PortError(Exception):
    """Base exception for Port.io API errors."""
    pass

class PortAuthError(PortError):
    """Exception raised for authentication errors."""
    pass

def setup_logging():
    """Configure logging to stderr."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )
    return logging.getLogger(__name__)
