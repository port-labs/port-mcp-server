import pytest

from src.models.actions import Action
from src.tools.action import GetActionTool


@pytest.fixture
def mock_client_with_action(mock_client):
    """Add specific return values for this test"""
    mock_client.get_action.return_value = Action(
        identifier="test-action",
        title="Test Action",
        description="Test action description",
        trigger={
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        invocationMethod={"type": "WEBHOOK", "url": "https://example.com/webhook"},
    )
    return mock_client


@pytest.mark.asyncio
async def test_get_action_tool(mock_client_with_action):
    """Test the GetActionTool's metadata and function execution."""
    # Create the tool
    tool = GetActionTool(mock_client_with_action)

    # Test tool metadata
    assert tool.name == "get_action"
    assert "action" in tool.description.lower()

    # Test function execution
    schema = {"action_identifier": "test-action"}
    result = await tool.get_action(tool.validate_input(schema))
    mock_client_with_action.get_action.assert_awaited_once_with("test-action")
    assert result is not None
    assert result["identifier"] == "test-action"
    assert result["title"] == "Test Action"
