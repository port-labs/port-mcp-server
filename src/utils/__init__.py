"""Utility functions for the Port MCP Server."""

# Import and re-export setup_logging function
from .errors import PortAuthError, PortError
from .logger import get_logger

# For backward compatibility, create a logger getter that can be accessed as an attribute
class LoggerProxy:
    def __getattr__(self, name):
        logger = get_logger()
        return getattr(logger, name)

logger = LoggerProxy()

from .schema import inline_schema

__all__ = ["logger", "PortError", "PortAuthError", "inline_schema"]
