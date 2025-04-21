"""Port MCP server.

This module provides an MCP server for interacting with Port.io.
"""

__version__ = "0.1.0"

from .server import main
from .client import PortClient
from .resources import register_all as register_all_resources
from .prompts import register_all as register_all_prompts

__all__ = [
    "main",
    "PortClient",
    "register_all_resources",
    "register_all_prompts",
] 