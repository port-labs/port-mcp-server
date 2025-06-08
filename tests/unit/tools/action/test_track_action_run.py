import pytest
from unittest.mock import AsyncMock

from src.models.action_run import ActionRun
from src.tools.action import TrackActionRunTool


@pytest.fixture
def mock_client_for_track_action_run(mock_client):
    """Add specific return values for this test"""
    # Mock a completed action run
    completed_action_run = ActionRun.construct(
        id="run-123",
        status="SUCCESS",
        action={"identifier": "test-action", "title": "Test Action"},
        createdAt="2023-12-01T10:00:00Z",
        endedAt="2023-12-01T10:05:00Z",
    )

    mock_client.get_action_run.return_value = completed_action_run

    return mock_client


@pytest.fixture
def mock_client_for_track_in_progress(mock_client):
    """Add specific return values for tracking an in-progress action run"""
    # First call returns in-progress, second call returns success
    in_progress_run = ActionRun.construct(
        id="run-456",
        status="IN_PROGRESS",
        action={"identifier": "test-action", "title": "Test Action"},
        createdAt="2023-12-01T10:00:00Z",
    )

    completed_run = ActionRun.construct(
        id="run-456",
        status="SUCCESS",
        action={"identifier": "test-action", "title": "Test Action"},
        createdAt="2023-12-01T10:00:00Z",
        endedAt="2023-12-01T10:05:00Z",
    )

    mock_client.get_action_run.side_effect = [in_progress_run, completed_run]

    return mock_client


@pytest.mark.asyncio
async def test_track_action_run_tool_completed(mock_client_for_track_action_run):
    """Test the TrackActionRunTool's metadata and function execution for completed run."""
    # Create the tool
    tool = TrackActionRunTool(mock_client_for_track_action_run)

    # Test tool metadata
    assert tool.name == "track_action_run"
    assert "track" in tool.description.lower()
    assert "action run" in tool.description.lower()

    # Test function execution for completed action run
    schema = {"run_id": "run-123"}
    result = await tool.track_action_run(tool.validate_input(schema))

    # Should call get_action_run at least once
    assert mock_client_for_track_action_run.get_action_run.awaited
    assert result is not None
    assert "action_run" in result
    assert result["action_run"]["id"] == "run-123"
    assert result["action_run"]["status"] == "SUCCESS"


@pytest.mark.asyncio
async def test_track_action_run_tool_with_poll_interval(mock_client_for_track_action_run):
    """Test the TrackActionRunTool with custom poll interval."""
    # Create the tool
    tool = TrackActionRunTool(mock_client_for_track_action_run)

    # Test function execution with custom poll interval
    schema = {"run_id": "run-123", "poll_interval": 5}
    result = await tool.track_action_run(tool.validate_input(schema))

    assert result is not None
    assert result["action_run"]["status"] == "SUCCESS"


@pytest.mark.asyncio
async def test_track_action_run_tool_failure_status(mock_client):
    """Test the TrackActionRunTool for failed action run."""
    # Mock a failed action run
    failed_action_run = ActionRun.construct(
        id="run-failed",
        status="FAILURE",
        action={"identifier": "test-action", "title": "Test Action"},
        createdAt="2023-12-01T10:00:00Z",
        endedAt="2023-12-01T10:05:00Z",
    )

    mock_client.get_action_run.return_value = failed_action_run

    # Create the tool
    tool = TrackActionRunTool(mock_client)

    # Test function execution for failed action run
    schema = {"run_id": "run-failed"}
    result = await tool.track_action_run(tool.validate_input(schema))

    assert result is not None
    assert result["action_run"]["status"] == "FAILURE"
