import pytest

from src.models.actions import Action
from src.tools.action import ListActionsTool


@pytest.fixture
def mock_client_with_actions(mock_client):
    """Add specific return values for this test"""
    from src.models.actions.action import ActionTrigger, ActionInvocationMethodWebhook
    mock_client.get_all_actions.return_value = [
        Action(
            identifier="test-action-1",
            title="Test Action 1",
            description="First test action",
            trigger=ActionTrigger(
                type="self-service",
                operation="CREATE",
                user_inputs={"properties": {}, "required": []},
            ),
            invocation_method=ActionInvocationMethodWebhook(type="WEBHOOK", url="https://example.com/webhook1"),
        ),
        Action(
            identifier="test-action-2",
            title="Test Action 2",
            description="Second test action",
            trigger=ActionTrigger(
                type="self-service",
                operation="DAY-2",
                user_inputs={"properties": {}, "required": []},
            ),
            invocation_method=ActionInvocationMethodWebhook(type="WEBHOOK", url="https://example.com/webhook2"),
        ),
    ]
    return mock_client


@pytest.mark.asyncio
async def test_list_actions_tool(mock_client_with_actions):
    """Test the ListActionsTool's metadata and function execution."""
    # Create the tool
    tool = ListActionsTool(mock_client_with_actions)

    # Test tool metadata
    assert tool.name == "list_actions"
    assert "actions" in tool.description.lower()

    # Test function execution
    schema = {"detailed": True, "trigger_type": "self-service"}
    result = await tool.list_actions(tool.validate_input(schema))
    mock_client_with_actions.get_all_actions.assert_awaited_once_with("self-service")
    assert result is not None
    assert "actions" in result
    assert len(result["actions"]) == 2
    assert result["actions"][0]["identifier"] == "test-action-1"
    assert result["actions"][1]["identifier"] == "test-action-2"


@pytest.mark.asyncio
async def test_list_actions_tool_with_defaults(mock_client_with_actions):
    """Test the ListActionsTool with default parameters."""
    # Create the tool
    tool = ListActionsTool(mock_client_with_actions)

    # Test function execution with defaults
    schema = {}
    result = await tool.list_actions(tool.validate_input(schema))
    mock_client_with_actions.get_all_actions.assert_awaited_once_with("self-service")
    assert result is not None
