"""Scorecard-related tools for Port MCP server."""

import logging
import json
from typing import Any, Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

def register(mcp: FastMCP, port_client: Any) -> None:
    """
    Register scorecard tools with the FastMCP server.
    
    Args:
        mcp: The FastMCP server instance
        port_client: The Port client instance
        
    Scorecard model provides these methods:
        - to_summary(): Returns just the basic information like title, identifier, blueprint
        - to_text(detailed=False): Returns summary view (same as to_summary())
        - to_text(detailed=True): Returns detailed view (with rules, calculation method, and timestamps)
    """
    
    @mcp.tool()
    async def get_scorecards(detailed: bool = False) -> str:
        """
        Retrieve all scorecards from Port.
        
        Args:
            detailed: If True, returns complete scorecard details including rules and calculation method.
                     If False (default), returns summary information only.
        
        Returns:
            A formatted text representation of all scorecards.
            Summary format includes title, identifier and blueprint.
            Detailed format includes rules, calculation method, and timestamps.
        """
        try:
            logger.info(f"Retrieving all scorecards from Port (detailed={detailed})")
            scorecards = await port_client.get_all_scorecards()
            return scorecards.to_text(detailed=detailed) if hasattr(scorecards, 'to_text') else str(scorecards)
        except Exception as e:
            logger.error(f"Error in get_scorecards: {str(e)}", exc_info=True)
            # Pass along the full error message without truncating it
            error_message = str(e)
            return f"❌ Error retrieving scorecards: {error_message}"
            
    @mcp.tool()
    async def get_scorecard(scorecard_id: str, blueprint_id: str = None, detailed: bool = True) -> str:
        """
        Retrieve information about a specific scorecard by its identifier.
        
        Args:
            scorecard_id: The unique identifier of the scorecard to retrieve
            blueprint_id: The identifier of the blueprint the scorecard belongs to.
                        If not provided, will try to find it from the list of scorecards.
            detailed: If True (default), returns complete scorecard details.
                     If False, returns summary information only.
            
        Returns:
            A formatted text representation of the scorecard.
            Summary format includes title, identifier and blueprint.
            Detailed format includes rules, calculation method, and timestamps.
        """
        try:
            logger.info(f"Retrieving scorecard '{scorecard_id}' (detailed={detailed})")
            
            if blueprint_id:
                logger.info(f"Blueprint ID provided: {blueprint_id}")
                
            scorecard = await port_client.get_scorecard_details(scorecard_id, blueprint_id)
            return scorecard.to_text(detailed=detailed) if hasattr(scorecard, 'to_text') else str(scorecard)
        except Exception as e:
            logger.error(f"Error in get_scorecard: {str(e)}", exc_info=True)
            # Pass along the full error message without truncating it
            error_message = str(e)
            return f"❌ Error retrieving scorecard '{scorecard_id}': {error_message}"
    
    @mcp.tool()
    async def create_scorecard(
        blueprint_id: str,
        identifier: str,
        title: str,
        levels: List[Dict[str, str]],
        rules: List[Dict[str, Any]] = None,
        description: str = None
    ) -> str:
        """
        Create a new scorecard for a specific blueprint.
        
        Args:
            blueprint_id: The identifier of the blueprint to create the scorecard for
            identifier: The unique identifier for the new scorecard
            title: The display title of the scorecard
            levels: List of levels for the scorecard, each with "title" and "color" properties
                   The first level is the base level and should not have rules associated with it
                   Example: [{"title": "Basic", "color": "blue"}, {"title": "Silver", "color": "silver"}]
            rules: Optional list of rules for the scorecard
                  Each rule should have at minimum: identifier, title, level, and query properties
                  The level must match one of the levels defined in the levels parameter (except the first level)
                  Example rule: {
                    "identifier": "has-team",
                    "title": "Has responsible team",
                    "level": "Silver",
                    "query": {
                      "combinator": "and",
                      "conditions": [{"property": "$team", "operator": "isNotEmpty"}]
                    }
                  }
            description: Optional description for the scorecard
            
        Returns:
            A formatted text representation of the created scorecard if successful
            An error message if creation failed
        """
        try:
            # Validate that rules don't reference the first level (base level)
            if rules:
                base_level = levels[0]["title"] if levels else None
                for rule in rules:
                    if rule.get("level") == base_level:
                        return f"❌ Error creating scorecard: The base level '{base_level}' cannot have rules associated with it."
            
            # Prepare the scorecard data
            scorecard_data = {
                "identifier": identifier,
                "title": title,
                "levels": levels,
                "rules": rules or []
            }
            
            if description:
                scorecard_data["description"] = description
            
            logger.info(f"Creating scorecard '{identifier}' for blueprint '{blueprint_id}'")
            logger.debug(f"Scorecard data: {json.dumps(scorecard_data, indent=2)}")
            
            # Create the scorecard
            created_scorecard = await port_client.create_new_scorecard(blueprint_id, scorecard_data)
            
            # Return the created scorecard details
            return (
                f"✅ Successfully created scorecard '{title}' (ID: {identifier})\n\n"
                f"{created_scorecard.to_text(detailed=True) if hasattr(created_scorecard, 'to_text') else str(created_scorecard)}"
            )
        except Exception as e:
            logger.error(f"Error in create_scorecard: {str(e)}", exc_info=True)
            # Pass along the full error message without truncating it
            error_message = str(e)
            return f"❌ Error creating scorecard '{identifier}' for blueprint '{blueprint_id}': {error_message}"
    
    @mcp.tool()
    async def delete_scorecard(scorecard_id: str, blueprint_id: str) -> str:
        """
        Delete a scorecard from Port.
        
        Args:
            scorecard_id: The unique identifier of the scorecard to delete
            blueprint_id: The identifier of the blueprint the scorecard belongs to
            
        Returns:
            A success message if deletion was successful
            An error message if deletion failed
        """
        try:
            logger.info(f"Deleting scorecard '{scorecard_id}' from blueprint '{blueprint_id}'")
            
            # First verify that the scorecard exists
            try:
                await port_client.get_scorecard_details(scorecard_id, blueprint_id)
            except Exception as e:
                logger.warning(f"Scorecard '{scorecard_id}' not found or not accessible: {str(e)}")
                return f"❌ Cannot delete scorecard '{scorecard_id}': Scorecard not found or not accessible"
            
            # Delete the scorecard
            result = await port_client.delete_scorecard(scorecard_id, blueprint_id)
            
            if result:
                return f"✅ Successfully deleted scorecard '{scorecard_id}' from blueprint '{blueprint_id}'"
            else:
                return f"❌ Failed to delete scorecard '{scorecard_id}'. No error was reported, but the operation may not have succeeded."
        except Exception as e:
            logger.error(f"Error in delete_scorecard: {str(e)}", exc_info=True)
            # Pass along the full error message without truncating it
            error_message = str(e)
            return f"❌ Error deleting scorecard '{scorecard_id}': {error_message}" 