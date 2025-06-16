"""User-Agent header utility for Port MCP server."""


def get_user_agent(mcp_client: str = "unknown", version: str = "0.2.7") -> str:
    """
    Build User-Agent header for HTTP requests.
    
    Format: "port-mcp-server/{mcp_client}/{version}"
    Where:
    - mcp_client: The client using the MCP server (e.g., vscode, cursor)
    - version: The current Port MCP version
    
    Args:
        mcp_client: The MCP client name (defaults to "unknown")
        version: The Port MCP server version (defaults to current version)
    
    Returns:
        str: Formatted User-Agent header value
    """
    # Import here to avoid circular imports during initialization
    try:
        from src.config import config
        mcp_client = config.mcp_client
    except (ImportError, AttributeError):
        # Fallback if config is not available
        pass
    
    try:
        # Import version here to avoid circular imports
        import importlib.metadata
        version = importlib.metadata.version("mcp-server-port")
    except (ImportError, Exception):
        # Fallback to hardcoded version if package metadata is not available
        try:
            # Try to read from src.__init__.py if available
            import re
            import os
            init_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "__init__.py")
            if os.path.exists(init_path):
                with open(init_path, 'r') as f:
                    content = f.read()
                    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
                    if match:
                        version = match.group(1)
        except Exception:
            # Final fallback
            version = "0.2.7"
    
    return f"port-mcp-server/{mcp_client}/{version}"