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
        
    Note on Blueprint Format:
        Resources are available in two formats with separate endpoints:
        - Summary format: Basic information only (title, identifier, description)
        - Detailed format: Full information including schema properties and relations
        
        Available endpoints:
        - port-blueprints: - List of all blueprints in summary format
        - port-blueprints-detailed: - List of all blueprints in detailed format
        - port-blueprint://{blueprint_identifier} - Specific blueprint in detailed format
        - port-blueprint-summary://{blueprint_identifier} - Specific blueprint in summary format
    """
    
    async def _get_all_blueprints(detailed: bool = False) -> str:
        logger.info(f"Resource: Retrieving all blueprints from Port (detailed={detailed})")
        blueprints = await port_client.get_blueprints()
        return blueprints.to_text(detailed=detailed) if hasattr(blueprints, 'to_text') else str(blueprints)
    
    async def _get_blueprint(blueprint_identifier: str, detailed: bool = False) -> str:
        logger.info(f"Resource: Retrieving blueprint with identifier: {blueprint_identifier} (detailed={detailed})")
        blueprint = await port_client.get_blueprint(blueprint_identifier)
        return blueprint.to_text(detailed=detailed) if hasattr(blueprint, 'to_text') else str(blueprint)
    
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
            - Title and identifier for each blueprint
            - Description (if available)
            - Schema properties with titles, types, and formats
            - Relations with target blueprints and cardinality
            - Creation/update timestamps (if available)
        """
        try:
            return await _get_all_blueprints(detailed=True)
        except Exception as e:
            logger.error(f"Error in get_all_blueprints_detailed resource: {str(e)}", exc_info=True)
            return f"❌ Error retrieving detailed blueprints: {str(e)}"

    @mcp.resource("port-blueprint://{blueprint_identifier}")
    async def get_specific_blueprint(blueprint_identifier: str) -> str:
        """
        Get detailed information about a specific blueprint.
        
        Path parameters:
            blueprint_identifier: The unique identifier of the blueprint
            
        Returns:
            A formatted text representation of the blueprint in detailed format, including:
            - Title and identifier
            - Description (if available)
            - Schema properties with titles, types, and formats
            - Relations with target blueprints and cardinality
            - Creation/update timestamps (if available)
        """
        try:
            return await _get_blueprint(blueprint_identifier, detailed=True)
        except Exception as e:
            logger.error(f"Error in get_specific_blueprint resource: {str(e)}", exc_info=True)
            return f"❌ Error retrieving blueprint {blueprint_identifier}: {str(e)}"

    @mcp.resource("port-blueprint-summary://{blueprint_identifier}")
    async def get_specific_blueprint_summary(blueprint_identifier: str) -> str:
        """
        Get summary information about a specific blueprint.
        
        Path parameters:
            blueprint_identifier: The unique identifier of the blueprint
            
        Returns:
            A formatted text representation of the blueprint in summary format, including:
            - Title and identifier
            - Description (if available)
        """
        try:
            return await _get_blueprint(blueprint_identifier, detailed=False)
        except Exception as e:
            logger.error(f"Error in get_specific_blueprint_summary resource: {str(e)}", exc_info=True)
            return f"❌ Error retrieving blueprint summary {blueprint_identifier}: {str(e)}"
