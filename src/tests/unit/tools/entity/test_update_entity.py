import pytest

from src.server.models import Entity
from src.server.tools.entity import UpdateEntityTool


@pytest.fixture
def mock_client_for_update_entity(mock_client):
    """Add specific return values for this test"""
    mock_client.update_entity.return_value = Entity(identifier="test-entity", title="Updated Entity", blueprint="test-blueprint")
    return mock_client


@pytest.mark.asyncio
async def test_update_entity_tool(mock_client_for_update_entity):
    """Test the UpdateEntityTool's metadata and function execution."""
    # Create the tool
    tool = UpdateEntityTool(mock_client_for_update_entity)
    
    # Test tool metadata
    assert tool.name == "update_entity"
    assert "update" in tool.description.lower()
    assert "entity" in tool.description.lower()
    
    # Test function execution
    entity_data = {
        "identifier": "test-entity",
        "title": "Updated Entity",
        "properties": {}
    }
    schema = {
        "blueprint_identifier": "test-blueprint", 
        "entity_identifier": "test-entity",
        "entity": entity_data
    }
    result = await tool.update_entity(tool.validate_input(schema))
    mock_client_for_update_entity.update_entity.assert_awaited_once_with("test-blueprint", "test-entity", entity_data)
    assert result is not None 