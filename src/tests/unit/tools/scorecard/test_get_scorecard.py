import pytest
import sys
from unittest.mock import AsyncMock


from src.server.models import Scorecard
from src.server.tools.scorecard import GetScorecardTool


@pytest.fixture
def mock_client_with_scorecard(mock_client):
    """Add specific return values for this test"""
    mock_client.get_scorecard.return_value = Scorecard(
        identifier="test-scorecard", 
        title="Test Scorecard",
        rules=[],
        blueprint="test-blueprint",
        id="test-scorecard"
    )
    return mock_client


@pytest.mark.asyncio
async def test_get_scorecard_tool(mock_client_with_scorecard):
    """Test the GetScorecardTool's metadata and function execution."""
    # Create the tool
    tool = GetScorecardTool(mock_client_with_scorecard)
    
    # Test tool metadata
    assert tool.name == "get_scorecard"
    assert "scorecard" in tool.description.lower()
    assert "blueprint_identifier" in tool.input_schema.__annotations__
    assert "scorecard_identifier" in tool.input_schema.__annotations__
    
    # Test function execution
    schema = {
        "blueprint_identifier": "test-blueprint", 
        "scorecard_identifier": "test-scorecard", 
        "detailed": True
    }
    result = await tool.get_scorecard(tool.validate_input(schema))
    mock_client_with_scorecard.get_scorecard.assert_awaited_once_with("test-scorecard", "test-blueprint")
    assert result is not None 