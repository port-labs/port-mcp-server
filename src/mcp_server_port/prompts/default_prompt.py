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
- Scorecard management for measuring quality and compliance
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

- get_scorecards:
  - Lists all scorecards available in your Port installation
  - By default, returns scorecards in SUMMARY format (title, identifier, blueprint)
  - For full details of all scorecards, including rules and levels, use detailed=True
  - Example: "Show me all scorecards" or "List detailed scorecards with rules"

- get_scorecard:
  - Gets detailed information about a specific scorecard
  - Requires the scorecard identifier
  - Optionally accepts a blueprint_id parameter if you already know which blueprint the scorecard belongs to
  - Returns DETAILED format by default (with rules, levels, and metadata)
  - For summary only, use detailed=False
  - Example: "Show me details of the 'ProductionReadiness' scorecard" or "Get the 'Security' scorecard from the 'service' blueprint"

- create_scorecard:
  - Creates a new scorecard for a specific blueprint
  - Required parameters: blueprint_id, identifier, title, levels (list of level objects)
  - Optional parameters: rules (list of rule objects), description
  - IMPORTANT: The first level in the levels list is considered the base level and cannot have rules associated with it
  - Each level should have 'title' and 'color' properties
  - Each rule must reference a level from the levels list (except the base/first level)
  - Example: "Create a security compliance scorecard for the 'service' blueprint with Bronze, Silver, and Gold levels"

- delete_scorecard:
  - Deletes an existing scorecard
  - Required parameters: scorecard_id, blueprint_id
  - Use with caution as this operation is irreversible
  - Example: "Delete the 'TestScorecard' scorecard from the 'service' blueprint"

- invoke_ai_agent:
  - Interact with user-defined AI agents for complex queries or actions
  - Use for natural language interactions with Port data
  - Examples: "Which service has the highest scorecard level" or "Report a documentation issue"
  - Try other tools if this doesn't provide desired results

Recommended workflow for finding entity information:
1. Use get_blueprints (summary) to find the relevant blueprint identifier
2. Use get_entities (summary) with that blueprint ID to list available entities
3. Once you find the entity you're interested in, use get_entity (detailed) to see all its details

Recommended workflow for scorecard information:
1. Use get_scorecards (summary) to see all available scorecards
2. Use get_scorecard with the specific scorecard identifier to see its rules and levels

Recommended workflow for creating scorecards:
1. Use get_blueprint (detailed) to understand the properties available in a blueprint
2. Define appropriate levels (Basic, Bronze, Silver, Gold is a common pattern)
3. Create rules based on blueprint properties, ensuring the first level (Basic) doesn't have any rules
4. Use create_scorecard with the blueprint_id, defined levels and rules
5. Verify the scorecard was created using get_scorecard

Resource patterns:
- port-blueprints: - Summarized list of all blueprints
- port-blueprints-detailed: - Detailed list of all blueprints (with schema properties and relations)

Note: While tools offer parameter flexibility, resources provide fixed formats with dedicated endpoints.
"""
