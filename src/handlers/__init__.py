"""Port MCP server.

This module provides an MCP server for interacting with Port.io.
"""

__version__ = "0.1.0"

from .call_tool import execute_tool

__all__ = [
    "execute_tool",
]
