import pytest
from functools import partial

from unittest.mock import MagicMock, AsyncMock

from src.models.scorecards.scorecard import Scorecard
from src.tools.scorecard.get_scorecards import GetScorecardsTool


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def mock_client_with_scorecards(mock_client):
    """Add specific return values for this test"""
    mock_client.get_scorecards = AsyncMock(
        return_value=[
            Scorecard(
                identifier="test-scorecard",
                title="Test Scorecard",
                rules=[],
                blueprint="test-blueprint",
                id="test-scorecard",
            )
        ]
    )
    return mock_client


@pytest.mark.asyncio
async def test_get_scorecards_tool(mock_client_with_scorecards):
    # Test setup
    tool = GetScorecardsTool(port_client=mock_client_with_scorecards)
    # Test function execution
    schema = {"blueprint_identifier": "test-blueprint", "detailed": True}
    result = await tool.get_scorecards(tool.validate_input(schema))
    mock_client_with_scorecards.get_scorecards.assert_awaited_once_with("test-blueprint")
    assert result is not None
    assert result["scorecards"][0]["identifier"] == "test-scorecard"
