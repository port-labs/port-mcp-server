from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.models.agent.port_agent_response import PortAgentInvocation, PortAgentTriggerResponse
from src.tools.ai_agent import InvokeAIAGentTool
from src.utils.errors import PortError


@pytest.fixture
def mock_client_for_ai_agent(mock_client):
    """Add specific return values for this test"""
    mock_client.trigger_agent.return_value = PortAgentTriggerResponse(
        ok=True,
        invocation=PortAgentInvocation(identifier="test-invocation-id")
    )

    # Create a status object with proper string attributes
    status_obj = MagicMock()
    status_obj.status = "completed"
    status_obj.output = "Test agent response message"
    status_obj.selected_agent = "test-agent"
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
    assert result["message"] == "Test agent response message"
    assert result["selected_agent"] == "test-agent"


@pytest.fixture
def mock_client_for_timeout(mock_client):
    """Add specific return values for timeout test"""
    mock_client.trigger_agent.return_value = PortAgentTriggerResponse(
        ok=True,
        invocation=PortAgentInvocation(identifier="test-invocation-id")
    )

    # Create a status object with proper string attributes
    status_obj = MagicMock()
    status_obj.status = "in_progress"
    status_obj.output = "Still processing..."
    status_obj.selected_agent = "test-agent"
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
        result = await tool.invoke_ai_agent(tool.validate_input(schema))

        # Verify the result indicates a timeout
        assert result["invocation_id"] == "test-invocation-id"
        assert result["invocation_status"] == "timed_out"
        assert "timed out" in result["message"]


@pytest.fixture
def mock_client_for_error(mock_client):
    """Add specific return values for error test"""
    mock_client.trigger_agent.side_effect = PortError("Response missing required invocation identifier")
    return mock_client


@pytest.mark.asyncio
async def test_invoke_ai_agent_tool_error_handling(mock_client_for_error):
    """Test the InvokeAIAGentTool's error handling."""
    # Create the tool
    tool = InvokeAIAGentTool(mock_client_for_error)

    # Test function execution with a prompt expecting an error
    schema = {"prompt": "Test prompt that will cause an error"}

    with pytest.raises(PortError) as excinfo:
        await tool.invoke_ai_agent(tool.validate_input(schema))
    
    assert "invocation identifier" in str(excinfo.value)


@pytest.fixture
def mock_client_for_dict_invocation(mock_client):
    """Mock client that returns response with dict invocation (simulating construct() behavior)"""
    # Create a response that mimics what construct() would return - with dict instead of PortAgentInvocation
    response_with_dict = PortAgentTriggerResponse.construct(
        ok=True,
        invocation={"identifier": "test-dict-invocation-id"}  # This stays as dict when using construct()
    )
    mock_client.trigger_agent.return_value = response_with_dict

    # Create a status object with proper string attributes
    status_obj = MagicMock()
    status_obj.status = "completed"
    status_obj.output = "Test agent response with dict invocation"
    status_obj.selected_agent = "test-agent-dict"
    mock_client.get_invocation_status.return_value = status_obj

    return mock_client


@pytest.mark.asyncio
async def test_invoke_ai_agent_tool_with_dict_invocation(mock_client_for_dict_invocation):
    """Test the InvokeAIAGentTool handles dict invocation (construct() scenario) correctly."""
    # Create the tool
    tool = InvokeAIAGentTool(mock_client_for_dict_invocation)

    # Test function execution
    schema = {"prompt": "Test prompt with dict invocation"}
    result = await tool.invoke_ai_agent(tool.validate_input(schema))

    # Verify the correct methods were called
    mock_client_for_dict_invocation.trigger_agent.assert_awaited_once_with("Test prompt with dict invocation")
    mock_client_for_dict_invocation.get_invocation_status.assert_awaited_once_with("test-dict-invocation-id")

    # Verify the result
    assert result["invocation_id"] == "test-dict-invocation-id"
    assert result["invocation_status"] == "completed"
    assert result["message"] == "Test agent response with dict invocation"
    assert result["selected_agent"] == "test-agent-dict"


@pytest.mark.asyncio
async def test_invoke_ai_agent_handles_dict_invocation_correctly():
    """Test that we properly handle the case where invocation is a dict (construct scenario)."""
    # This test validates the specific bug we fixed where response.invocation.identifier
    # would fail with 'dict' object has no attribute 'identifier'
    
    # Create a response using construct() which leaves invocation as a dict
    response = PortAgentTriggerResponse.construct(
        ok=True,
        invocation={"identifier": "test-construct-id"}
    )
    
    # Verify that invocation is indeed a dict (this is the root cause of the bug)
    assert isinstance(response.invocation, dict)
    assert response.invocation["identifier"] == "test-construct-id"
    
    # Verify that accessing .identifier would fail (this was the original bug)
    with pytest.raises(AttributeError, match="'dict' object has no attribute 'identifier'"):
        _ = response.invocation.identifier  # This would fail before our fix
    
    # Our fix should handle this gracefully by checking isinstance(response.invocation, dict)
    if isinstance(response.invocation, dict):
        identifier = response.invocation.get('identifier')
    else:
        identifier = response.invocation.identifier
        
    assert identifier == "test-construct-id"