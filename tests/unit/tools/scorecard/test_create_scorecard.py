import pytest

from src.models import Scorecard
from src.tools.scorecard import CreateScorecardTool


@pytest.fixture
def mock_client_for_create_scorecard(mock_client):
    """Add specific return values for this test"""
    mock_client.create_scorecard.return_value = Scorecard(
        identifier="test-scorecard",
        title="New Scorecard",
        rules=[],
        blueprint="test-blueprint",
        id="test-scorecard",
    )
    return mock_client


@pytest.mark.asyncio
async def test_create_scorecard_tool(mock_client_for_create_scorecard):
    """Test the CreateScorecardTool's metadata and function execution."""
    # Create the tool
    tool = CreateScorecardTool(mock_client_for_create_scorecard)

    # Test tool metadata
    assert tool.name == "create_scorecard"
    assert "create" in tool.description.lower()
    assert "scorecard" in tool.description.lower()

    # Test function execution
    scorecard_data = {
        "identifier": "test-scorecard",
        "title": "New Scorecard",
        "blueprint_identifier": "test-blueprint",
        "rules": [],
        "calculation_method": "average",
    }
    result = await tool.create_scorecard(tool.validate_input(scorecard_data))
    mock_client_for_create_scorecard.create_scorecard.assert_awaited_once()
    assert result is not None
