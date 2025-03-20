"""Resources for Port MCP server.

This module aggregates all resources for the Port MCP server.
"""

from .blueprint_resources import register as register_blueprint_resources

def register_all(mcp, port_client):
    """Register all resources with the MCP server."""
    register_blueprint_resources(mcp, port_client)
