"""Blueprint-related tools for Port MCP server."""

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

def register(mcp: FastMCP, port_client: Any) -> None:
    """
    Register blueprint tools with the FastMCP server.
    
    Args:
        mcp: The FastMCP server instance
        port_client: The Port client instance
        
    Blueprint model provides these methods:
        - to_summary(): Always returns just the basic information like name, identifier, description
        - to_text(detailed=False): Returns summary view (same as to_summary())
        - to_text(detailed=True): Returns detailed view (with schema properties and relations)

    """
    @mcp.tool()
    async def get_blueprints(detailed: bool = False) -> str:
        """
        Retrieve a list of all blueprints from Port.
        
        Args:
            detailed: If True, returns complete schema details for each blueprint.
                     If False (default), returns summary information only.
        
        Returns:
            A formatted text representation of all available blueprints in your Port instance.
            Summary format includes title, identifier and description.
            Detailed format includes schema properties and relations as well.
        """
        try:
            logger.info(f"Retrieving all blueprints from Port (detailed={detailed})")
            blueprints = await port_client.get_blueprints()
            return blueprints.to_text(detailed=detailed) if hasattr(blueprints, 'to_text') else str(blueprints)
        except Exception as e:
            logger.error(f"Error in get_blueprints: {str(e)}", exc_info=True)
            return f"❌ Error retrieving blueprints: {str(e)}"
            
    @mcp.tool()
    async def get_blueprint(blueprint_identifier: str, detailed: bool = True) -> str:
        """
        Retrieve information about a specific blueprint by its identifier.
        
        Args:
            blueprint_identifier: The unique identifier of the blueprint to retrieve
            detailed: If True (default), returns complete schema details.
                     If False, returns summary information only.
            
        Returns:
            A formatted text representation of the blueprint.
            Summary format includes title, identifier and description.
            Detailed format includes schema properties and relations as well.
        """
        try:
            logger.info(f"Retrieving blueprint with identifier: {blueprint_identifier} (detailed={detailed})")
            blueprint = await port_client.get_blueprint(blueprint_identifier)
            return blueprint.to_text(detailed=detailed) if hasattr(blueprint, 'to_text') else str(blueprint)
        except Exception as e:
            logger.error(f"Error in get_blueprint: {str(e)}", exc_info=True)
            return f"❌ Error retrieving blueprint {blueprint_identifier}: {str(e)}"
