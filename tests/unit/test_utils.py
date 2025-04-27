from typing import Any

import pytest
from loguru import logger

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
