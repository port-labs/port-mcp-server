import pytest

from src.tools.action import DeleteActionTool


@pytest.fixture
def mock_client_with_delete_action(mock_client):
    """Add specific return values for delete action test"""
    mock_client.delete_action.return_value = True
    return mock_client


@pytest.mark.asyncio
async def test_delete_action_tool_metadata(mock_client_with_delete_action):
    """Test the DeleteActionTool's metadata."""
    tool = DeleteActionTool(mock_client_with_delete_action)
    
    # Test tool metadata
    assert tool.name == "delete_action"
    assert "delete" in tool.description.lower()
    assert "action" in tool.description.lower()
    assert tool.annotations.title == "Delete Action"
    assert tool.annotations.read_only_hint is False
    assert tool.annotations.destructive_hint is True
    assert tool.annotations.idempotent_hint is False
    assert tool.annotations.open_world_hint is True


@pytest.mark.asyncio
async def test_delete_action_tool_execution(mock_client_with_delete_action):
    """Test the DeleteActionTool's function execution."""
    tool = DeleteActionTool(mock_client_with_delete_action)
    
    # Test input schema
    input_data = {"action_identifier": "test-action"}
    
    # Test function execution
    result = await tool.delete_action(tool.validate_input(input_data))
    
    # Verify client method was called with correct identifier
    mock_client_with_delete_action.delete_action.assert_awaited_once_with("test-action")
    
    # Verify result
    assert result is not None
    assert result["success"] is True
    assert "test-action" in result["message"]
    assert "deleted successfully" in result["message"]


@pytest.mark.asyncio
async def test_delete_action_tool_with_complex_identifier(mock_client_with_delete_action):
    """Test deleting an action with complex identifier."""
    tool = DeleteActionTool(mock_client_with_delete_action)
    
    input_data = {"action_identifier": "complex-action-name_with.special-chars"}
    
    result = await tool.delete_action(tool.validate_input(input_data))
    
    # Verify client method was called with correct identifier
    mock_client_with_delete_action.delete_action.assert_awaited_once_with(
        "complex-action-name_with.special-chars"
    )
    
    # Verify result
    assert result["success"] is True
    assert "complex-action-name_with.special-chars" in result["message"]


@pytest.mark.asyncio
async def test_delete_action_tool_missing_identifier():
    """Test that DeleteActionTool raises ValueError when action_identifier is missing."""
    # Create a mock client (don't need to set up return values since we expect an error)
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    
    tool = DeleteActionTool(mock_client)
    
    # Test with empty identifier
    input_data = {"action_identifier": ""}
    
    with pytest.raises(ValueError, match="Action identifier is required"):
        await tool.delete_action(tool.validate_input(input_data))
    
    # Verify client method was not called
    mock_client.delete_action.assert_not_called()


@pytest.mark.asyncio
async def test_delete_action_tool_none_identifier():
    """Test that DeleteActionTool raises ValueError when action_identifier is None."""
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    
    tool = DeleteActionTool(mock_client)
    
    # Test with None identifier (simulate model_dump returning None)
    from unittest.mock import patch
    with patch.object(tool, 'validate_input') as mock_validate:
        mock_validate.return_value.model_dump.return_value = {"action_identifier": None}
        
        with pytest.raises(ValueError, match="Action identifier is required"):
            await tool.delete_action(mock_validate.return_value)
    
    # Verify client method was not called
    mock_client.delete_action.assert_not_called()


@pytest.mark.asyncio
async def test_delete_action_tool_client_returns_false(mock_client):
    """Test DeleteActionTool when client returns False."""
    # Mock client to return False (deletion failed)
    mock_client.delete_action.return_value = False
    
    tool = DeleteActionTool(mock_client)
    
    input_data = {"action_identifier": "failing-action"}
    
    result = await tool.delete_action(tool.validate_input(input_data))
    
    # Verify client method was called
    mock_client.delete_action.assert_awaited_once_with("failing-action")
    
    # Verify result still shows success (the tool returns success based on client result)
    assert result["success"] is False
    assert "failing-action" in result["message"]


@pytest.mark.asyncio
async def test_delete_action_tool_schema_validation():
    """Test that the DeleteActionTool properly validates input schema."""
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    
    tool = DeleteActionTool(mock_client)
    
    # Test with valid input
    valid_input = {"action_identifier": "valid-action"}
    validated = tool.validate_input(valid_input)
    assert validated.action_identifier == "valid-action"
    
    # Test with invalid input (missing required field)
    with pytest.raises(Exception):  # Should raise validation error
        tool.validate_input({})
    
    # Test with extra fields (should be ignored)
    extra_input = {
        "action_identifier": "valid-action",
        "extra_field": "should_be_ignored"
    }
    validated = tool.validate_input(extra_input)
    assert validated.action_identifier == "valid-action"
    assert not hasattr(validated, "extra_field") 