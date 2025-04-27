"""Error classes for Port.io MCP server."""


class PortError(Exception):
    """Base exception for Port.io API errors."""

    pass


class PortAuthError(PortError):
    """Exception raised for authentication errors."""

    pass
