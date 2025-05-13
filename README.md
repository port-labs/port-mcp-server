# Port MCP Server

A Model Context Protocol (MCP) server for the [Port.io API](https://www.getport.io/), enabling Claude to interact with Port.io's developer platform capabilities using natural language.

## What You Can Do With Port MCP

Transform how you work with Port.io using natural language:

### Find Information Quickly
- **Get entity details** - "Who is the owner of service X?"
- **Check on-call status** - "Who is on call right now?"
- **Get catalog insights** - "How many services do we have in production?"

### Analyze Scorecards 
- **Identify weak points** - "Which services are failing for the gold level and why?"
- **Get compliance status** - "Show me all services that don't meet our security requirements"
- **Improve quality** - "What do I need to fix to reach the next scorecard level?"

### Create Resources
- **Build scorecards** - "Create a new scorecard called 'Security Posture' with levels Basic, Silver, and Gold"
- **Define rules** - "Add a rule that requires services to have a team owner to reach the Silver level"
- **Setup quality gates** - "Create a rule that checks if services have proper documentation"

We're continuously expanding Port MCP's capabilities. Have a suggestion? We'd love to hear your feedback on our [roadmap](https://roadmap.getport.io/ideas)!

## Installation

### Obtain your Port credentials
1. Create a Port.io Account:
   - Visit [Port.io](https://www.port.io/)
   - Sign up for an account if you don't have one

2. Create an API Key:
   - Navigate to your Port.io dashboard
   - Go to Settings > Credentials
   - Save both the Client ID and Client Secret

### Claude Desktop

Add the following to your `claude_desktop_config.json`:


#### Docker
```json
{
  "mcpServers": {
    "port": {
      "command": "docker",
      "args": [
               "run",
                "-i",
                "--rm",
                "-e",
                "PORT_CLIENT_ID",
                "-e",
                "PORT_CLIENT_SECRET",
                "-e",
                "PORT_REGION",
                "-e",
                "PORT_LOG_LEVEL",
                "ghcr.io/port-labs/port-mcp-server:0.2.1"
              ],
              "env": {
                "PORT_CLIENT_ID": "<PORT_CLIENT_ID>",
                "PORT_CLIENT_SECRET": "<PORT_CLIENT_SECRET>",
                "PORT_REGION": "<PORT_REGION>",
                "PORT_LOG_LEVEL": "<PORT_LOG_LEVEL>"
              }
    }
  }
}
```


### Cursor

Configure in Cursor settings:
   - Go to Cursor settings > MCP Servers
   - Configure with:
     * Name - `Port`
     * Type - `Command`
     * Command - `/path/to/your/file/run-port-mcp.sh`

####Docker

```json
{
    "mcpServers": {
        "port": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e",
                "PORT_CLIENT_ID",
                "-e",
                "PORT_CLIENT_SECRET",
                "-e",
                "PORT_REGION",
                "-e",
                "PORT_LOG_LEVEL",
                "ghcr.io/port-labs/port-mcp-server:0.2.1"
            ],
            "env": {
                "PORT_CLIENT_ID": "<PORT_CLIENT_ID>",
                "PORT_CLIENT_SECRET": "<PORT_CLIENT_SECRET>",
                "PORT_REGION": "<PORT_REGION>",
                "PORT_LOG_LEVEL": "<PORT_LOG_LEVEL>"
            }
        }
    }
}
```
![Cursor MCP Screenshot](/assets/cursor_mcp_screenshot.png)


## Available Tools

### Blueprint Tools

1. `get_blueprints`
   - Retrieve a list of all blueprints from Port
   - Optional inputs:
     - `detailed` (boolean, default: false): Return complete schema details for each blueprint
   - Returns: Formatted text representation of all available blueprints

2. `get_blueprint`
   - Retrieve information about a specific blueprint by its identifier
   - Required inputs:
     - `blueprint_identifier` (string): The unique identifier of the blueprint to retrieve
   - Optional inputs:
     - `detailed` (boolean, default: true): Return complete schema details

3. `create_blueprint`
   - Create a new blueprint in Port
   - Required inputs:
     - Various fields including identifier, title, properties, etc.
   - Returns: The created blueprint object

4. `update_blueprint`
   - Update an existing blueprint
   - Required inputs:
     - `identifier` (string): The unique identifier of the blueprint to update
     - Various fields to update
   - Returns: The updated blueprint object

5. `delete_blueprint`
   - Delete a blueprint from Port
   - Required inputs:
     - `blueprint_identifier` (string): The unique identifier of the blueprint to delete
   - Returns: Success status

### Entity Tools

1. `get_entities`
   - Retrieve all entities for a given blueprint
   - Required inputs:
     - `blueprint_identifier` (string): The identifier of the blueprint to get entities for
   - Optional inputs:
     - `detailed` (boolean, default: false): Return complete entity details including properties

2. `get_entity`
   - Retrieve information about a specific entity
   - Required inputs:
     - `blueprint_identifier` (string): The identifier of the blueprint the entity belongs to
     - `entity_identifier` (string): The unique identifier of the entity to retrieve
   - Optional inputs:
     - `detailed` (boolean, default: true): Return complete entity details

3. `create_entity`
   - Create a new entity for a specific blueprint
   - Required inputs:
     - `blueprint_identifier` (string): The identifier of the blueprint to create the entity for
     - `entity` (object): The entity data following the blueprint schema

4. `update_entity`
   - Update an existing entity
   - Required inputs:
     - `blueprint_identifier` (string): The identifier of the blueprint the entity belongs to
     - `entity_identifier` (string): The unique identifier of the entity to update
     - `entity` (object): The updated entity data

5. `delete_entity`
   - Delete an entity
   - Required inputs:
     - `blueprint_identifier` (string): The identifier of the blueprint the entity belongs to
     - `entity_identifier` (string): The unique identifier of the entity to delete
   - Optional inputs:
     - `delete_dependents` (boolean, default: false): If true, also deletes all dependencies

### Scorecard Tools

1. `get_scorecards`
   - Retrieve all scorecards from Port
   - Optional inputs:
     - `detailed` (boolean, default: false): Return complete scorecard details

2. `get_scorecard`
   - Retrieve information about a specific scorecard by its identifier
   - Required inputs:
     - `scorecard_id` (string): The unique identifier of the scorecard to retrieve
     - `blueprint_id` (string, optional): The identifier of the blueprint the scorecard belongs to

3. `create_scorecard`
   - Create a new scorecard for a specific blueprint
   - Required inputs:
     - `blueprint_id` (string): The identifier of the blueprint to create the scorecard for
     - `identifier` (string): The unique identifier for the new scorecard
     - `title` (string): The display title of the scorecard
     - `levels` (list): List of levels for the scorecard
   - Optional inputs:
     - `rules` (list): List of rules for the scorecard
     - `description` (string): Description for the scorecard

4. `update_scorecard`
   - Update an existing scorecard
   - Required inputs:
     - `blueprint_identifier` (string): The identifier of the blueprint the scorecard belongs to
     - `scorecard_identifier` (string): The unique identifier of the scorecard to update
     - Various fields to update (title, levels, rules, etc.)
   - Returns: The updated scorecard object

5. `delete_scorecard`
   - Delete a scorecard from Port
   - Required inputs:
     - `blueprint_identifier` (string): The identifier of the blueprint the scorecard belongs to
     - `scorecard_identifier` (string): The unique identifier of the scorecard to delete
   - Returns: Success status

### AI Agent Tool

1. `invoke_ai_agent`
   - Invoke a Port AI agent with a specific prompt
   - Required inputs:
     - `prompt` (string): The prompt to send to the AI agent
   - Returns: Invocation status and message from the AI agent

## Feedback and Roadmap

We're continuously improving Port MCP and would love to hear from you! Please share your feedback and feature requests on our [roadmap page](https://roadmap.getport.io/ideas).

## Troubleshooting

If you encounter authentication errors, verify that:
1. Your Port credentials are correctly set in the arguments
2. You have the necessary permissions
3. The credentials are properly copied to your configuration

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.