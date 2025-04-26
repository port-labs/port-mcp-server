import pytest

from src.models import Blueprint
from src.tools.blueprint import CreateBlueprintTool


@pytest.fixture
def mock_client_for_create(mock_client):
    """Add specific return values for this test"""
    mock_client.create_blueprint.return_value = Blueprint(
        identifier="new-blueprint",
        title="New Blueprint",
        icon="Template",
        schema={"properties": {"name": {"title": "Name", "type": "string"}}, "required": ["name"]},
    )
    return mock_client


@pytest.mark.asyncio
async def test_create_blueprint_tool(mock_client_for_create):
    """Test the CreateBlueprintTool's metadata and function execution."""
    # Create the tool
    tool = CreateBlueprintTool(mock_client_for_create)

    # Test tool metadata
    assert tool.name == "create_blueprint"
    assert "create" in tool.description.lower()
    assert "blueprint" in tool.description.lower()

    # Test function execution
    blueprint_data = {
        "identifier": "new-blueprint",
        "title": "New Blueprint",
        "icon": "Template",
        "schema": {
            "properties": {"name": {"title": "Name", "type": "string"}},
            "required": ["name"],
        },
    }
    result = await tool.create_blueprint(tool.validate_input(blueprint_data))
    mock_client_for_create.create_blueprint.assert_awaited_once()
    assert result is not None
