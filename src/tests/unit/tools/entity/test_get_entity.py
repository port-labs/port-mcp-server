import pytest
import sys
from unittest.mock import AsyncMock


from src.server.models import Entity
from src.server.tools.entity import GetEntityTool


@pytest.fixture
def mock_client_with_entity(mock_client):
    """Add specific return values for this test"""
    mock_client.get_entity.return_value = Entity(identifier="test-entity", title="Test Entity", blueprint="test-blueprint")
    return mock_client


@pytest.mark.asyncio
async def test_get_entity_tool(mock_client_with_entity):
    """Test the GetEntityTool's metadata and function execution."""
    # Create the tool
    tool = GetEntityTool(mock_client_with_entity)
    
    # Test tool metadata
    assert tool.name == "get_entity"
    assert "Get an entity" in tool.description
    assert "blueprint_identifier" in tool.input_schema.__annotations__
    assert "entity_identifier" in tool.input_schema.__annotations__
    
    # Test function execution
    schema = {"blueprint_identifier": "test-blueprint", "entity_identifier": "test-entity", "detailed": True}
    result = await tool.get_entity(tool.validate_input(schema))
    mock_client_with_entity.get_entity.assert_awaited_once_with("test-blueprint", "test-entity")
    assert result is not None 