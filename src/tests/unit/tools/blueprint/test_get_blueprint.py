import pytest
import sys
from unittest.mock import AsyncMock


from src.server.models import Blueprint
from src.server.tools.blueprint import GetBlueprintTool


@pytest.fixture
def mock_client_with_blueprint(mock_client):
    """Add specific return values for this test"""
    mock_client.get_blueprint.return_value = Blueprint(
        identifier="test-blueprint", 
        title="Test Blueprint", 
        icon="Template",
        schema={
            "properties": {},
            "required": []
        }
    )
    return mock_client


@pytest.mark.asyncio
async def test_get_blueprint_tool(mock_client_with_blueprint):
    """Test the GetBlueprintTool's metadata and function execution."""
    # Create the tool
    tool = GetBlueprintTool(mock_client_with_blueprint)
    
    # Test tool metadata
    assert tool.name == "get_blueprint"
    assert "blueprint" in tool.description.lower()
    
    # Test function execution
    schema = {"blueprint_identifier": "test-blueprint"}
    result = await tool.get_blueprint(tool.validate_input(schema))
    mock_client_with_blueprint.get_blueprint.assert_awaited_once_with("test-blueprint")
    assert result is not None 