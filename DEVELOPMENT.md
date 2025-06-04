# Development Environment Setup

This guide will help you set up a simple Docker-based development environment for the Port MCP Server.

## Prerequisites

1. **Docker**: Make sure you have Docker installed on your system.
2. **Port.io Credentials**: You'll need your Port Client ID and Client Secret from your Port.io account.

## Quick Setup

### 1. Build the Development Image

```bash
# Build the development Docker image (only need to do this once, or after dependency changes)
docker build -f Dockerfile.dev -t port-mcp-dev .
```

### 2. Configure Cursor

Add this to your Cursor MCP settings with your actual Port.io credentials:

```json
{
  "mcpServers": {
    "port-dev": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v", "/home/daniel/port-mcp-server/src:/app/src",
        "-v", "/home/daniel/port-mcp-server/tests:/app/tests",
        "-v", "/home/daniel/port-mcp-server/pyproject.toml:/app/pyproject.toml",
        "-v", "/home/daniel/port-mcp-server/poetry.lock:/app/poetry.lock",
        "-e", "PORT_CLIENT_ID=your_actual_client_id",
        "-e", "PORT_CLIENT_SECRET=your_actual_client_secret",
        "-e", "PORT_REGION=EU",
        "-e", "PORT_LOG_LEVEL=DEBUG",
        "-e", "PYTHONPATH=/app",
        "port-mcp-dev"
      ]
    }
  }
}
```

**That's it!** Each time Cursor connects, it will:
- Run a fresh container with your latest code
- Mount your source code as volumes for instant updates
- Automatically clean up the container when done

## Development Workflow

1. **Edit Code**: Make changes to files in the `src/` directory
2. **Test Immediately**: Cursor automatically uses your latest code on each connection
3. **No Restart Needed**: Volume mounts ensure changes are immediate

## Useful Commands

### Build Development Image
```bash
docker build -f Dockerfile.dev -t port-mcp-dev .
```

### Rebuild After Dependency Changes
```bash
docker build -f Dockerfile.dev -t port-mcp-dev . --no-cache
```

### Manual Test (with your credentials)
```bash
docker run --rm -i \
  -v "$(pwd)/src:/app/src" \
  -v "$(pwd)/tests:/app/tests" \
  -v "$(pwd)/pyproject.toml:/app/pyproject.toml" \
  -v "$(pwd)/poetry.lock:/app/poetry.lock" \
  -e PORT_CLIENT_ID=your_client_id \
  -e PORT_CLIENT_SECRET=your_client_secret \
  -e PORT_REGION=EU \
  -e PYTHONPATH=/app \
  port-mcp-dev
```

### Run Tests
```bash
docker run --rm -i \
  -v "$(pwd)/src:/app/src" \
  -v "$(pwd)/tests:/app/tests" \
  -v "$(pwd)/pyproject.toml:/app/pyproject.toml" \
  -v "$(pwd)/poetry.lock:/app/poetry.lock" \
  -e PYTHONPATH=/app \
  port-mcp-dev \
  poetry run pytest
```

### Access Container Shell for Debugging
```bash
docker run --rm -it \
  -v "$(pwd)/src:/app/src" \
  -v "$(pwd)/tests:/app/tests" \
  -v "$(pwd)/pyproject.toml:/app/pyproject.toml" \
  -v "$(pwd)/poetry.lock:/app/poetry.lock" \
  -e PYTHONPATH=/app \
  port-mcp-dev \
  bash
```

## Features

- ✅ **Ultra Simple**: Just build once, use everywhere
- ✅ **No Container Management**: Containers auto-cleanup after each use
- ✅ **Instant Code Updates**: Volume mounts make changes immediate
- ✅ **Poetry Integration**: Uses your existing Poetry configuration
- ✅ **Secure**: Credentials only in Cursor configuration
- ✅ **Self-Contained**: No docker-compose or persistent containers

## Troubleshooting

### Image Build Fails
- Check Docker is running
- Ensure you're in the project root directory
- Check build logs for specific errors

### MCP Connection Issues
- Verify the Docker image exists: `docker images | grep port-mcp-dev`
- Test manually with the command above
- Check that volume paths in Cursor config match your actual paths

### Code Changes Not Reflected
- Verify you're editing files in the correct `src/` directory
- Check volume mount paths in your Cursor configuration
- The `-v "/home/daniel/port-mcp-server/src:/app/src"` path should match your actual project location

### Authentication Errors
- Double-check your PORT_CLIENT_ID and PORT_CLIENT_SECRET
- Verify your Port.io region (EU or US)
- Ensure credentials have necessary permissions

## Path Configuration

**Important**: Update the volume mount paths in your Cursor configuration to match your actual project location:

- Replace `/home/daniel/port-mcp-server/` with your actual project path
- You can find your current path with: `pwd`

## Why This Setup Is Better

- **🎯 Simpler**: No docker-compose, no persistent containers
- **🔒 Secure**: Credentials only in Cursor
- **⚡ Fast**: Volume mounts make code changes instant
- **🧹 Clean**: Containers automatically cleaned up
- **🔄 Reliable**: Fresh container every time eliminates state issues

This is the cleanest possible setup - just build once and use! 