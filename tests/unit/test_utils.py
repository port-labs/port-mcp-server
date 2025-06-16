from typing import Any

import pytest
from src.utils import logger

from src.utils.logger import setup_logging
from src.utils.schema import inline_schema


def test_setup_logging():
    """Test that setup_logging returns a logger with the expected name."""
    log = setup_logging()

    assert isinstance(log, type(logger))


@pytest.mark.parametrize(
    "schema",
    [
        {
            "$defs": {},
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        },
        {
            "$defs": {},
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        },
    ],
)
def test_inline_schema(schema: dict[str, Any]):
    """Test that inline_schema returns a schema with the expected name."""
    assert schema["$defs"] is not None
    schema = inline_schema(schema)

    assert isinstance(schema, dict)
    assert schema.get("$defs", None) is None


def test_get_user_agent():
    """Test that get_user_agent returns the correct format."""
    # Import the function directly to avoid circular imports
    from src.utils.user_agent import get_user_agent
    
    # Test with explicit parameters to avoid config dependencies
    user_agent = get_user_agent('vscode', '0.2.7')
    
    # Should match format: "port-mcp-server/{mcp_client}/{version}"
    assert user_agent == "port-mcp-server/vscode/0.2.7"
    
    parts = user_agent.split("/")
    assert len(parts) == 3
    assert parts[0] == "port-mcp-server"
    assert parts[1] == "vscode"
    assert parts[2] == "0.2.7"
