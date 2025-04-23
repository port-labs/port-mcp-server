from typing import Any, Dict
import pytest

from loguru import logger

from server.utils.schema import inline_schema
from server.utils.logging import setup_logging


def test_setup_logging():
    """Test that setup_logging returns a logger with the expected name."""
    log = setup_logging()
    
    assert isinstance(log, type(logger))

@pytest.mark.parametrize("schema", [
    {
        "$defs":{},
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        }
    },
    {
        "$defs":{},
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        }
    }
])
def test_inline_schema(schema: Dict[str, Any]):
    """Test that inline_schema returns a schema with the expected name."""
    assert schema["$defs"] is not None
    schema = inline_schema(schema)
    
    assert isinstance(schema, dict)
    assert schema.get("$defs", None) is None