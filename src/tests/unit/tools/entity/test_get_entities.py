import pytest
import sys
from unittest.mock import AsyncMock


from src.server.models import Entity
from src.server.tools.entity import GetEntitiesTool


@pytest.fixture
def mock_client_with_entities(mock_client):
    """Add specific return values for this test"""
    mock_client.get_entities.return_value = [Entity(identifier="test-entity", blueprint="test-blueprint")]
    return mock_client


@pytest.mark.asyncio
async def test_get_entities_tool(mock_client_with_entities):
    """Test the GetEntitiesTool's metadata and function execution."""
    # Create the tool
    tool = GetEntitiesTool(mock_client_with_entities)
    
    # Test tool metadata
    assert tool.name == "get_entities"
    assert "entities" in tool.description.lower()
    
    # Test function execution
    schema = {"blueprint_identifier": "test-blueprint", "detailed": True}
    result = await tool.get_entities(tool.validate_input(schema))
    mock_client_with_entities.get_entities.assert_awaited_once_with("test-blueprint")
    assert result is not None 