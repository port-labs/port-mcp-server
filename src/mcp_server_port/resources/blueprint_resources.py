"""Blueprint-related resources for Port MCP server."""

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

def register(mcp: FastMCP, port_client: Any) -> None:
    """
    Register blueprint resources with the FastMCP server.
    
    Args:
        mcp: The FastMCP server instance
        port_client: The Port client instance

    Available endpoints:
    - port-blueprints: - List of all blueprints in summary format (title, identifier, description)
    - port-blueprints-detailed: - List of all blueprints in detailed format (title, identifier, description, schema properties, and relations)
    """
    
    async def _get_all_blueprints(detailed: bool = False) -> str:
        logger.info(f"Resource: Retrieving all blueprints from Port (detailed={detailed})")
        blueprints = await port_client.get_blueprints()
        return blueprints.to_text(detailed=detailed) if hasattr(blueprints, 'to_text') else str(blueprints)
       
    @mcp.resource("port-blueprints:")
    async def get_all_blueprints_summary() -> str:
        """
        List all available blueprints in Port (summary format).
        
        Returns:
            A formatted text representation of all blueprints in summary format:
            - Title and identifier for each blueprint
            - Description (if available)
        """
        try:
            return await _get_all_blueprints(detailed=False)
        except Exception as e:
            logger.error(f"Error in get_all_blueprints_summary resource: {str(e)}", exc_info=True)
            return f"❌ Error retrieving blueprints: {str(e)}"

    @mcp.resource("port-blueprints-detailed:")
    async def get_all_blueprints_detailed() -> str:
        """
        List all available blueprints in Port with complete details.
        
        Returns:
            A formatted text representation of all blueprints in detailed format, including:
            - Title, identifier, description for each blueprint
            - Schema properties with titles, types, and formats
            - Relations with target blueprints and cardinality
        """
        try:
            return await _get_all_blueprints(detailed=True)
        except Exception as e:
            logger.error(f"Error in get_all_blueprints_detailed resource: {str(e)}", exc_info=True)
            return f"❌ Error retrieving detailed blueprints: {str(e)}"