import pytest

from src.tools.entity import DeleteEntityTool


@pytest.fixture
def mock_client_for_delete_entity(mock_client):
    """Add specific return values for this test"""
    mock_client.delete_entity.return_value = {"success": True}
    return mock_client


@pytest.mark.asyncio
async def test_delete_entity_tool(mock_client_for_delete_entity):
    """Test the DeleteEntityTool's metadata and function execution."""
    # Create the tool
    tool = DeleteEntityTool(mock_client_for_delete_entity)

    # Test tool metadata
    assert tool.name == "delete_entity"
    assert "delete" in tool.description.lower()
    assert "entity" in tool.description.lower()

    # Test function execution
    schema = {"blueprint_identifier": "test-blueprint", "entity_identifier": "test-entity"}
    result = await tool.delete_entity(tool.validate_input(schema))
    mock_client_for_delete_entity.delete_entity.assert_called_once_with("test-blueprint", "test-entity", False)
    assert result is not None
