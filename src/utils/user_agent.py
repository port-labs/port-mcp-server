"""User-Agent header utility for Port MCP server."""

import re
from pathlib import Path


def get_user_agent(version: str | None = None) -> str:
    """
    Build User-Agent header for HTTP requests.
    
    Format: "port-mcp-server/{version}"
    Where:
    - version: The current Port MCP version
    
    Args:
        version: The Port MCP server version (optional, auto-detected if not provided)
    
    Returns:
        str: Formatted User-Agent header value
    """
    if version is None:
        version = _get_version()
    
    return f"port-mcp-server/{version}"


def _get_version() -> str:
    """
    Get the version from pyproject.toml or fallback to unknown.
    
    Returns:
        str: Version string or "unknown" if not found
    """
    try:
        project_root = Path(__file__).parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'\[project\].*?version\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL)
                if match:
                    return match.group(1)
    except Exception:
        pass
    
    try:
        import importlib.metadata
        return importlib.metadata.version("mcp-server-port")
    except (ImportError, Exception):
        pass
    
    return "unknown"