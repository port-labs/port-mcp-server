# Port MCP Server

The [Port IO](https://www.getport.io/) MCP server is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server, enabling advanced automations and natural language interactions for developers and AI applications.

## Quick Start

**Prerequisites:**
- Port account with [Client ID and Secret](https://app.port.io/) from Settings > Credentials
- Either [Docker](https://www.docker.com/get-started/) or [uvx](https://pypi.org/project/uvx/) installed

## Key Capabilities

- **Entity Management** - Query and manage your Port catalog: "Who owns service X?" or "Show production services"
- **Scorecard Analysis** - Assess compliance and quality: "Which services fail security requirements?"
- **Resource Creation** - Build scorecards and rules through natural language
- **RBAC & Permissions** - Configure access controls and approval workflows

💡 [Share feedback on our roadmap](https://roadmap.getport.io/ideas)

## Installation

### Option 1: Docker (Recommended)

```bash
# Set environment variables
export PORT_CLIENT_ID="your_client_id"
export PORT_CLIENT_SECRET="your_client_secret" 
export PORT_REGION="EU"  # or "US"

# Run the container
docker run -i --rm \
  -e PORT_CLIENT_ID \
  -e PORT_CLIENT_SECRET \
  -e PORT_REGION \
  ghcr.io/port-labs/port-mcp-server:latest
```

### Option 2: Package Installation (uvx)

```bash
# Install and run
uvx mcp-server-port --client-id your_client_id --client-secret your_client_secret --region EU
```

### Windows Support

**PowerShell:**
```powershell
$env:PORT_CLIENT_ID="your_client_id"
$env:PORT_CLIENT_SECRET="your_client_secret"
$env:PORT_REGION="EU"

docker run -i --rm -e PORT_CLIENT_ID -e PORT_CLIENT_SECRET -e PORT_REGION ghcr.io/port-labs/port-mcp-server:latest
```

### Configuration Options

| Parameter | UVX Flag | Environment Variable | Default |
|-----------|----------|---------------------|---------|
| Log Level | `--log-level` | `PORT_LOG_LEVEL` | `ERROR` |
| Log Path | N/A | `PORT_LOG_PATH` | `/tmp/port-mcp.log` |
| API Validation | `--api-validation-enabled` | `PORT_API_VALIDATION_ENABLED` | `False` |


## Client Integration

> [!TIP] Use the full path to Docker (e.g., `/usr/local/bin/docker`) if you encounter PATH issues.

### Claude Desktop

Edit your `claude_desktop_config.json` file:

<details>
<summary>Docker Configuration</summary>

```json
{
  "mcpServers": {
    "port": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "PORT_CLIENT_ID",
        "-e", "PORT_CLIENT_SECRET", 
        "-e", "PORT_REGION",
        "ghcr.io/port-labs/port-mcp-server:latest"
      ],
      "env": {
        "PORT_CLIENT_ID": "<YOUR_CLIENT_ID>",
        "PORT_CLIENT_SECRET": "<YOUR_CLIENT_SECRET>",
        "PORT_REGION": "<YOUR_REGION>"
      }
    }
  }
}
```
</details>

<details>
<summary>uvx Configuration</summary>

```json
{
  "mcpServers": {
    "Port": {
      "command": "uvx",
      "args": [
        "mcp-server-port@0.2.8",
        "--client-id", "<PORT_CLIENT_ID>",
        "--client-secret", "<PORT_CLIENT_SECRET>",
        "--region", "<PORT_REGION>"
      ],
      "env": {
        "PORT_CLIENT_ID": "<YOUR_CLIENT_ID>",
        "PORT_CLIENT_SECRET": "<YOUR_CLIENT_SECRET>",
        "PORT_REGION": "<YOUR_REGION>"
      }
    }
  }
}
```
</details>

### Other Clients

<details>
<summary>Cursor</summary>

Add to your `mcp.json` configuration - use the same JSON format as Claude Desktop above.
</details>

<details>
<summary>VS Code</summary>

Quick install links:
- [Docker setup](https://insiders.vscode.dev/redirect/mcp/install?name=port&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22-e%22%2C%22PORT_CLIENT_ID%22%2C%22-e%22%2C%22PORT_CLIENT_SECRET%22%2C%22-e%22%2C%22PORT_REGION%22%2C%22ghcr.io%2Fport-labs%2Fport-mcp-server%3Alatest%22%5D%2C%22env%22%3A%7B%22PORT_CLIENT_ID%22%3A%22%3CPORT_CLIENT_ID%3E%22%2C%22PORT_CLIENT_SECRET%22%3A%22%3CPORT_CLIENT_SECRET%3E%22%2C%22PORT_REGION%22%3A%22%3CPORT_REGION%3E%22%7D%7D)
- [uvx setup](https://insiders.vscode.dev/redirect/mcp/install?name=port&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22mcp-server-port%400.2.8%22%2C%22--client-id%22%2C%22%3CPORT_CLIENT_ID%3E%22%2C%22--client-secret%22%2C%22%3CPORT_CLIENT_SECRET%3E%22%2C%22--region%22%2C%22%3CPORT_REGION%3E%22%5D%2C%22env%22%3A%7B%22PORT_CLIENT_ID%22%3A%22%3CPORT_CLIENT_ID%3E%22%2C%22PORT_CLIENT_SECRET%22%3A%22%3CPORT_CLIENT_SECRET%3E%22%2C%22PORT_REGION%22%3A%22%3CPORT_REGION%3E%22%7D%7D)

Manual: Add to `settings.json` under `mcp.servers` with `"type": "stdio"` prefix.
</details>

<details>
<summary>Neovim (mcphub.nvim)</summary>

Use [mcphub.nvim](https://ravitemer.github.io/mcphub.nvim/) plugin. Add to `~/.config/mcphub/servers.json` - same JSON format as Claude Desktop above.
</details>

## Available Tools

### Blueprint Tools
- `get_blueprints` - List all blueprints
- `get_blueprint` - Get specific blueprint details
- `create_blueprint` - Create new blueprint
- `update_blueprint` - Update existing blueprint
- `delete_blueprint` - Delete blueprint

### Entity Tools  
- `get_entities` - List entities for a blueprint
- `get_entity` - Get specific entity details
- `create_entity` - Create new entity
- `update_entity` - Update existing entity
- `delete_entity` - Delete entity

### Scorecard Tools
- `get_scorecards` - List all scorecards
- `get_scorecard` - Get specific scorecard
- `create_scorecard` - Create new scorecard
- `update_scorecard` - Update existing scorecard
- `delete_scorecard` - Delete scorecard

### AI Agent Tool
- `invoke_ai_agent` - Invoke Port AI agent with prompts

## Local Development

For local development and testing:

1. Clone the repository and run `make install`
2. Configure your MCP client to use your local version:

```json
{
  "mcpServers": {
    "port_local": {
      "command": "/path/to/your/port-mcp-server/.venv/bin/python",
      "args": ["-m", "src", "--client-id", "<YOUR_CLIENT_ID>", "--client-secret", "<YOUR_SECRET>", "--region", "<YOUR_REGION>"],
      "env": {
        "PORT_CLIENT_ID": "<YOUR_CLIENT_ID>",
        "PORT_CLIENT_SECRET": "<YOUR_SECRET>", 
        "PORT_REGION": "<YOUR_REGION>",
        "PYTHONPATH": "/path/to/your/port-mcp-server"
      }
    }
  }
}
```

## Troubleshooting

**Authentication Issues:**
- Verify credentials are correct and have necessary permissions
- Check that environment variables are properly set

**Windows-Specific Issues:**
- Use Windows-style paths for `PORT_LOG_PATH`: `C:\temp\port-mcp.log`
- Ensure Docker Desktop is running with Linux containers
- Check that `entrypoint.sh` has Unix line endings (LF)

**Environment Variables:**
```powershell
# PowerShell
$env:PORT_CLIENT_ID="your_client_id"
$env:PORT_CLIENT_SECRET="your_client_secret"
```

```cmd
# Command Prompt  
set PORT_CLIENT_ID=your_client_id
set PORT_CLIENT_SECRET=your_client_secret
```

## License

This MCP server is licensed under the MIT License. See [LICENSE](https://github.com/port-labs/port-mcp-server/blob/main/LICENSE) for details.

---

💡 [Share feedback and requests on our roadmap](https://roadmap.getport.io/ideas)
