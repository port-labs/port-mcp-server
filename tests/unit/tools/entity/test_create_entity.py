import pytest

from src.models import Entity
from src.tools.entity import CreateEntityTool


@pytest.fixture
def mock_client_for_create_entity(mock_client):
    """Add specific return values for this test"""
    mock_client.create_entity.return_value = Entity(identifier="new-entity", title="New Entity", blueprint="test-blueprint")
    return mock_client


@pytest.mark.asyncio
async def test_create_entity_tool(mock_client_for_create_entity):
    """Test the CreateEntityTool's metadata and function execution."""
    # Create the tool
    tool = CreateEntityTool(mock_client_for_create_entity)

    # Test tool metadata
    assert tool.name == "create_entity"
    assert "create" in tool.description.lower()
    assert "entity" in tool.description.lower()

    # Test function execution
    entity_data = {"identifier": "new-entity", "title": "New Entity", "properties": {}}
    schema = {
        "blueprint_identifier": "test-blueprint",
        "entity": entity_data,
        "query": {"upsert": False, "merge": False},
    }
    result = await tool.create_entity(tool.validate_input(schema))
    mock_client_for_create_entity.create_entity.assert_awaited_once()
    assert result is not None
