"""Utility functions for the Port MCP Server."""

# Import and re-export setup_logging function
from .errors import PortAuthError, PortError
from .logger import get_logger
from .schema import inline_schema

# For backward compatibility, expose logger as a function call
logger = get_logger()

__all__ = ["logger", "PortError", "PortAuthError", "inline_schema"]
