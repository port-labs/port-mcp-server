import pytest
from unittest.mock import AsyncMock

from src.server.models import Scorecard
from src.server.tools.scorecard import UpdateScorecardTool


@pytest.fixture
def mock_client_for_update_scorecard(mock_client):
    """Add specific return values for this test"""
    mock_client.update_scorecard.return_value = Scorecard(
        identifier="test-scorecard", 
        title="Updated Scorecard",
        rules=[],
        blueprint="test-blueprint",
        id="test-scorecard"
    )
    return mock_client


@pytest.mark.asyncio
async def test_update_scorecard_tool(mock_client_for_update_scorecard):
    """Test the UpdateScorecardTool's metadata and function execution."""
    # Create the tool
    tool = UpdateScorecardTool(mock_client_for_update_scorecard)
    
    # Test tool metadata
    assert tool.name == "update_scorecard"
    assert "update" in tool.description.lower()
    assert "scorecard" in tool.description.lower()
    
    # Test function execution
    schema = {
        "identifier": "test-scorecard",
        "title": "Updated Scorecard",
        "rules": [],
        "blueprint_identifier": "test-blueprint",
        "scorecard_identifier": "test-scorecard",
        "calculation_method": "average"
    }
    result = await tool.update_scorecard(tool.validate_input(schema))
    mock_client_for_update_scorecard.update_scorecard.assert_awaited_once()
    assert result is not None 