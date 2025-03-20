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
- Blueprint discovery and schema exploration
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

- invoke_ai_agent:
  - Interact with user-defined AI agents for complex queries or actions
  - Use for natural language interactions with Port data
  - Examples: "Which service has the highest scorecard level" or "Report a documentation issue"
  - Try other tools if this doesn't provide desired results

Resource patterns:
- port-blueprints: - List of all blueprints (summary)
- port-blueprints-detailed: - List of all blueprints (detailed)
- port-blueprint://{blueprint_identifier} - Specific blueprint (detailed)
- port-blueprint-summary://{blueprint_identifier} - Specific blueprint (summary)

Note: While tools offer parameter flexibility, resources provide fixed formats with dedicated endpoints.
"""
