import pytest

from src.models import Blueprint
from src.tools.blueprint import GetBlueprintsTool


@pytest.fixture
def mock_client_with_blueprints(mock_client):
    """Add specific return values for this test"""
    mock_client.get_blueprints.return_value = [
        Blueprint(
            identifier="test-blueprint",
            title="Test Blueprint",
            icon="Template",
            schema={"properties": {}, "required": []},
        )
    ]
    return mock_client


@pytest.mark.asyncio
async def test_get_blueprints_tool(mock_client_with_blueprints):
    """Test the GetBlueprintsTool's metadata and function execution."""
    # Create the tool
    tool = GetBlueprintsTool(mock_client_with_blueprints)

    # Test tool metadata
    assert tool.name == "get_blueprints"
    assert "Get all" in tool.description
    assert "blueprint" in tool.description.lower()

    # Test function execution
    schema = {"detailed": True}
    result = await tool.get_blueprints(tool.validate_input(schema))
    mock_client_with_blueprints.get_blueprints.assert_awaited_once()
    assert "blueprints" in result
