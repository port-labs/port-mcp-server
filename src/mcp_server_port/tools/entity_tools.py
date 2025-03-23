"""Entity-related tools for Port MCP server."""

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

def register(mcp: FastMCP, port_client: Any) -> None:
    """
    Register entity tools with the FastMCP server.
    
    Args:
        mcp: The FastMCP server instance
        port_client: The Port client instance
        
    Entity model provides these methods:
        - to_summary(): Always returns just the basic information like title, identifier, blueprint
        - to_text(detailed=False): Returns summary view (same as to_summary())
        - to_text(detailed=True): Returns detailed view (with properties, relations, and timestamps)
    """
    
    @mcp.tool()
    async def get_entities(blueprint_identifier: str, detailed: bool = False) -> str:
        """
        Retrieve all entities for a specific blueprint from Port.
        
        Args:
            blueprint_identifier: The identifier of the blueprint to get entities for
            detailed: If True, returns complete entity details including properties and relations.
                     If False (default), returns summary information only.
        
        Returns:
            A formatted text representation of all entities for the specified blueprint.
            Summary format includes title, identifier and blueprint.
            Detailed format includes properties, relations, and timestamps.
        """
        try:
            logger.info(f"Retrieving entities for blueprint '{blueprint_identifier}' from Port (detailed={detailed})")
            entities = await port_client.get_entities(blueprint_identifier)
            return entities.to_text(detailed=detailed) if hasattr(entities, 'to_text') else str(entities)
        except Exception as e:
            logger.error(f"Error in get_entities: {str(e)}", exc_info=True)
            return f"❌ Error retrieving entities for blueprint '{blueprint_identifier}': {str(e)}"
            
    @mcp.tool()
    async def get_entity(blueprint_identifier: str, entity_identifier: str, detailed: bool = True) -> str:
        """
        Retrieve information about a specific entity by its identifier.
        
        Args:
            blueprint_identifier: The identifier of the blueprint the entity belongs to
            entity_identifier: The unique identifier of the entity to retrieve
            detailed: If True (default), returns complete entity details.
                     If False, returns summary information only.
            
        Returns:
            A formatted text representation of the entity.
            Summary format includes title, identifier and blueprint.
            Detailed format includes properties, relations, and timestamps.
        """
        try:
            logger.info(f"Retrieving entity '{entity_identifier}' from blueprint '{blueprint_identifier}' (detailed={detailed})")
            entity = await port_client.get_entity(blueprint_identifier, entity_identifier)
            return entity.to_text(detailed=detailed) if hasattr(entity, 'to_text') else str(entity)
        except Exception as e:
            logger.error(f"Error in get_entity: {str(e)}", exc_info=True)
            return f"❌ Error retrieving entity '{entity_identifier}' from blueprint '{blueprint_identifier}': {str(e)}"
        