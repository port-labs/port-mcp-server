"""Prompts for Port MCP server.

This module contains prompts for the Port MCP server.
"""

from .default_prompt import register as register_default_prompt

def register_all(mcp):
    """Register all prompts with the MCP server."""
    register_default_prompt(mcp)
