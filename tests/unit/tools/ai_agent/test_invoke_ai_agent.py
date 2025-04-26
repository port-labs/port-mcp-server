from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.tools.ai_agent import InvokeAIAGentTool


@pytest.fixture
def mock_client_for_ai_agent(mock_client):
    """Add specific return values for this test"""
    mock_client.trigger_agent.return_value = {"invocation": {"identifier": "test-invocation-id"}}

    # Create a status object with a status attribute
    status_obj = MagicMock()
    status_obj.status = "completed"
    mock_client.get_invocation_status.return_value = status_obj

    return mock_client


@pytest.mark.asyncio
async def test_invoke_ai_agent_tool(mock_client_for_ai_agent):
    """Test the InvokeAIAGentTool's metadata and function execution."""
    # Create the tool
    tool = InvokeAIAGentTool(mock_client_for_ai_agent)

    # Test tool metadata
    assert tool.name == "invoke_ai_agent"
    assert "ai agent" in tool.description.lower()
    assert "prompt" in tool.input_schema.__annotations__

    # Test function execution
    schema = {"prompt": "Test prompt for AI agent"}
    result = await tool.invoke_ai_agent(tool.validate_input(schema))

    # Verify the correct methods were called
    mock_client_for_ai_agent.trigger_agent.assert_awaited_once_with("Test prompt for AI agent")
    mock_client_for_ai_agent.get_invocation_status.assert_awaited_once_with("test-invocation-id")

    # Verify the result
    assert result["invocation_id"] == "test-invocation-id"
    assert result["invocation_status"] == "completed"


@pytest.fixture
def mock_client_for_timeout(mock_client):
    """Add specific return values for timeout test"""
    mock_client.trigger_agent.return_value = {"invocation": {"identifier": "test-invocation-id"}}

    # Create a status object with a status attribute
    status_obj = MagicMock()
    status_obj.status = "in_progress"
    mock_client.get_invocation_status.return_value = status_obj

    return mock_client


@pytest.mark.asyncio
async def test_invoke_ai_agent_tool_timeout(mock_client_for_timeout):
    """Test the InvokeAIAGentTool's timeout behavior."""
    # Create the tool
    tool = InvokeAIAGentTool(mock_client_for_timeout)

    # Mock the asyncio.sleep to avoid actual delay in tests
    with patch("asyncio.sleep", AsyncMock()):
        # Test function execution with a prompt
        schema = {"prompt": "Test prompt that will timeout"}
        result = await tool.invoke_ai_agent(schema)

        # Verify the result indicates a timeout
        assert result["invocation_id"] == "test-invocation-id"
        assert result["invocation_status"] == "timed_out"
        assert "timed out" in result["message"]


@pytest.fixture
def mock_client_for_error(mock_client):
    """Add specific return values for error test"""
    mock_client.trigger_agent.return_value = {"error": "Something went wrong"}
    return mock_client


@pytest.mark.asyncio
async def test_invoke_ai_agent_tool_error_handling(mock_client_for_error):
    """Test the InvokeAIAGentTool's error handling."""
    # Create the tool
    tool = InvokeAIAGentTool(mock_client_for_error)

    # Test function execution with a prompt expecting an error
    schema = {"prompt": "Test prompt that will cause an error"}

    # The function should raise an exception when it can't get an identifier
    with pytest.raises(Exception) as excinfo:
        await tool.invoke_ai_agent(schema)

    # Verify the error message
    assert "Could not get invocation identifier" in str(excinfo.value)
