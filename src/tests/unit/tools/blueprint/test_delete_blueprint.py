import pytest
import sys
from unittest.mock import AsyncMock



from src.server.tools.blueprint import DeleteBlueprintTool


@pytest.fixture
def mock_client_for_delete(mock_client):
    """Add specific return values for this test"""
    mock_client.delete_blueprint.return_value = {"success": True}
    return mock_client


@pytest.mark.asyncio
async def test_delete_blueprint_tool(mock_client_for_delete):
    """Test the DeleteBlueprintTool's metadata and function execution."""
    # Create the tool
    tool = DeleteBlueprintTool(mock_client_for_delete)
    
    # Test tool metadata
    assert tool.name == "delete_blueprint"
    assert "delete" in tool.description.lower()
    assert "blueprint" in tool.description.lower()
    
    # Test function execution
    schema = {"blueprint_identifier": "test-blueprint"}
    result = await tool.delete_blueprint(tool.validate_input(schema))
    mock_client_for_delete.delete_blueprint.assert_awaited_once_with("test-blueprint")
    assert result is not None 