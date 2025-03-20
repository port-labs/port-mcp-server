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
        
    Note on Blueprint Format:
        The Blueprint model provides multiple representation methods:
        - to_summary(): Always returns just the basic information
        - to_text(detailed=False): Returns summary view (same as to_summary())
        - to_text(detailed=True): Returns detailed view (default for individual blueprints)
        
        The BlueprintList model follows the same pattern, with detailed=False as default.
        
        Summary format includes:
        - Title and identifier
        - Description (if available)
        
        Detailed format includes all summary fields plus:
        - Schema properties with title, type, and format
        - Relations with target blueprint, title, and cardinality
        - Creation/update information when available
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
            
            Summary format (default) includes:
            - Title and identifier for each blueprint
            - Description (if available)
            
            Detailed format includes all summary fields plus:
            - Schema properties with title, type, and format
            - Relations with target blueprint, title, and cardinality
            - Creation/update information when available
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
            A formatted text representation of the specified blueprint.
            
            Summary format includes:
            - Title and identifier
            - Description (if available)
            
            Detailed format (default) includes all summary fields plus:
            - Schema properties with title, type, and format
            - Relations with target blueprint, title, and cardinality
            - Creation/update information when available
        """
        try:
            logger.info(f"Retrieving blueprint with identifier: {blueprint_identifier} (detailed={detailed})")
            blueprint = await port_client.get_blueprint(blueprint_identifier)
            return blueprint.to_text(detailed=detailed) if hasattr(blueprint, 'to_text') else str(blueprint)
        except Exception as e:
            logger.error(f"Error in get_blueprint: {str(e)}", exc_info=True)
            return f"❌ Error retrieving blueprint {blueprint_identifier}: {str(e)}"
