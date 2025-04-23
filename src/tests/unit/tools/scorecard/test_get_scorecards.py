import pytest
import sys
from unittest.mock import AsyncMock


from src.server.models import Scorecard
from src.server.tools.scorecard import GetScorecardsTool


@pytest.fixture
def mock_client_with_scorecards(mock_client):
    """Add specific return values for this test"""
    mock_client.get_scorecards.return_value = [
        Scorecard(
            identifier="test-scorecard", 
            title="Test Scorecard",
            rules=[],
            blueprint="test-blueprint",
            id="test-scorecard"
        )
    ]
    return mock_client


@pytest.mark.asyncio
async def test_get_scorecards_tool(mock_client_with_scorecards):
    """Test the GetScorecardsTool's metadata and function execution."""
    # Create the tool
    tool = GetScorecardsTool(mock_client_with_scorecards)
    
    # Test tool metadata
    assert tool.name == "get_scorecards"
    assert "scorecards" in tool.description.lower()
    
    # Test function execution
    schema = {"blueprint_identifier": "test-blueprint", "detailed": True}
    result = await tool.get_scorecards(tool.validate_input(schema))
    mock_client_with_scorecards.get_scorecards.assert_awaited_once_with("test-blueprint")
    assert result is not None 