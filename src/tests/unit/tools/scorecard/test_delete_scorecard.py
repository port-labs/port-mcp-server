import pytest
import sys
from unittest.mock import AsyncMock



from src.server.tools.scorecard import DeleteScorecardTool


@pytest.fixture
def mock_client_for_delete_scorecard(mock_client):
    """Add specific return values for this test"""
    mock_client.delete_scorecard.return_value = {"success": True}
    return mock_client


@pytest.mark.asyncio
async def test_delete_scorecard_tool(mock_client_for_delete_scorecard):
    """Test the DeleteScorecardTool's metadata and function execution."""
    # Create the tool
    tool = DeleteScorecardTool(mock_client_for_delete_scorecard)
    
    # Test tool metadata
    assert tool.name == "delete_scorecard"
    assert "delete" in tool.description.lower()
    assert "scorecard" in tool.description.lower()
    
    # Test function execution
    schema = {
        "scorecard_identifier": "test-scorecard",
        "blueprint_identifier": "test-blueprint"
    }
    result = await tool.delete_scorecard(tool.validate_input(schema))
    mock_client_for_delete_scorecard.delete_scorecard.assert_awaited_once_with("test-scorecard", "test-blueprint")
    assert result is not None 