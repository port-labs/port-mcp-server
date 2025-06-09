import pytest

from src.models.action_run import ActionRun
from src.tools.action import RunActionTool


@pytest.fixture
def mock_client_for_run_action(mock_client):
    """Add specific return values for this test"""
    mock_client.create_global_action_run.return_value = ActionRun.construct(
        id="run-123",
        status="IN_PROGRESS",
        action={"identifier": "test-action", "title": "Test Action"},
        createdAt="2023-12-01T10:00:00Z",
    )
    mock_client.create_blueprint_action_run.return_value = ActionRun.construct(
        id="run-456",
        status="IN_PROGRESS",
        action={"identifier": "test-action", "title": "Test Action"},
        createdAt="2023-12-01T10:00:00Z",
    )
    mock_client.create_entity_action_run.return_value = ActionRun.construct(
        id="run-789",
        status="IN_PROGRESS",
        action={"identifier": "test-action", "title": "Test Action"},
        createdAt="2023-12-01T10:00:00Z",
    )

    # Set up action_runs attribute to avoid None check failure
    mock_client.action_runs = mock_client

    return mock_client


@pytest.mark.asyncio
async def test_run_action_tool_global(mock_client_for_run_action):
    """Test the RunActionTool's metadata and global action execution."""
    # Create the tool
    tool = RunActionTool(mock_client_for_run_action)

    # Test tool metadata
    assert tool.name == "run_action"
    assert "run" in tool.description.lower()
    assert "action" in tool.description.lower()

    # Test function execution for global action
    schema = {"action_identifier": "test-action", "properties": {"test_prop": "test_value"}}
    result = await tool.run_action(tool.validate_input(schema))
    mock_client_for_run_action.create_global_action_run.assert_awaited_once_with(
        action_identifier="test-action", properties={"test_prop": "test_value"}
    )
    assert result is not None
    assert "action_run" in result
    assert result["action_run"]["id"] == "run-123"


async def test_run_action_tool_entity(mock_client_for_run_action):
    """Test the RunActionTool for entity-specific action execution."""
    # Create the tool
    tool = RunActionTool(mock_client_for_run_action)

    # Test function execution for entity action
    schema = {
        "action_identifier": "test-action",
        "entity_identifier": "test-entity",
        "properties": {},
    }
    result = await tool.run_action(tool.validate_input(schema))
    mock_client_for_run_action.create_entity_action_run.assert_awaited_once_with(
        action_identifier="test-action",
        properties={},
        entity="test-entity",
    )
    assert result is not None
    assert result["action_run"]["id"] == "run-789"
