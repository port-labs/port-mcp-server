# Port MCP Server

MCP Server for the Port.io API, enabling Claude to interact with Port.io's AI agent.

## Tools

1. `get_port_token`
   - Get a Port.io authentication token
   - No inputs required
   - Returns: Authentication token with expiration information

2. `trigger_port_agent`
   - Trigger the Port.io AI agent with a prompt and wait for completion
   - Required inputs:
     - `prompt` (string): The prompt to send to the Port.io AI agent
   - Returns: Agent response with status, output, and any required actions
   - Note: The agent may return action URLs for bug reports or other tasks that require user interaction

## Setup

1. Create a Port.io Account:
   - Visit [Port.io](https://www.getport.io/)
   - Sign up for an account if you don't have one

2. Create an API Key:
   - Navigate to your Port.io dashboard
   - Go to Settings > Credentials
   - Save both the Client ID and Client Secret

### Usage with Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "port": {
      "command": "/path/to/your/venv/bin/python",
      "args": [
        "/path/to/port-mcp-server/src/mcp_server_port/server.py"
      ],
      "env": {
        "PORT_CLIENT_ID": "your-client-id",
        "PORT_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

### Troubleshooting

If you encounter authentication errors, verify that:
1. Your Port.io credentials are correctly set in the environment variables
2. The API key has the necessary permissions
3. The credentials are properly copied to your configuration

## Run

To run the server:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -e .

# Run server
python -m mcp_server_port
```

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.