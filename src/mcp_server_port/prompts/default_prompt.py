"""Default prompt for Port MCP server."""

from mcp.server.fastmcp import FastMCP

def register(mcp: FastMCP) -> None:
    """
    Register the default prompt with the FastMCP server.
    
    Args:
        mcp: The FastMCP server instance
    """
    @mcp.prompt()
    def server_instructions() -> str:
        """Port MCP server instructions."""
        return """This server provides access to Port, a developer portal platform. Use it to manage, query, and create resources.

Key capabilities:
- Blueprint and entity discovery
- Entity details and relationships
- AI agent interactions for complex operations
- Detailed schema introspection of Port resources

Tools:
- get_blueprints:
  - Returns a list of ALL available blueprints in your Port installation
  - By default, returns blueprints in SUMMARY format (title, identifier, description)
  - To get complete schema details for all blueprints at once, use detailed=True
  - Note: get_blueprints with detailed=True returns the same information as calling get_blueprint for each blueprint individually
  - Example: "Show me all blueprints" or "Show me detailed blueprints with relations and properties"

- get_blueprint:
  - Retrieves detailed information about a specific blueprint's schema
  - Requires the exact blueprint identifier
  - Returns DETAILED format by default (schema properties, relations, metadata)
  - For summary only, use detailed=False
  - Example: "Show me the schema for the 'service' blueprint"

- get_entities:
  - Lists all entities for a specific blueprint
  - Requires the blueprint identifier (use get_blueprints first to find it)
  - Returns SUMMARY format by default for better overview
  - Example: "List all entities in the 'service' blueprint"

- get_entity:
  - Gets detailed information about a specific entity
  - Requires both blueprint identifier and entity identifier
  - Returns DETAILED format by default
  - Example: "Show me details of entity 'backend-api' in blueprint 'service'"

- invoke_ai_agent:
  - Interact with user-defined AI agents for complex queries or actions
  - Use for natural language interactions with Port data
  - Examples: "Which service has the highest scorecard level" or "Report a documentation issue"
  - Try other tools if this doesn't provide desired results

Recommended workflow for finding entity information:
1. Use get_blueprints (summary) to find the relevant blueprint identifier
2. Use get_entities (summary) with that blueprint ID to list available entities
3. Once you find the entity you're interested in, use get_entity (detailed) to see all its details

Resource patterns:
- port-blueprints: - Summarized list of all blueprints
- port-blueprints-detailed: - Detailed list of all blueprints (with schema properties and relations)

Note: While tools offer parameter flexibility, resources provide fixed formats with dedicated endpoints.
"""
