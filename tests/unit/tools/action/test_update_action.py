import pytest

from src.models.actions import Action
from src.tools.action import UpdateActionTool


@pytest.fixture
def mock_client_with_update_action(mock_client):
    """Add specific return values for update action test"""
    mock_client.update_action.return_value = Action(
        identifier="test-action",
        title="Updated Test Action",
        description="Updated test action description",
        trigger={
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        invocationMethod={"type": "WEBHOOK", "url": "https://example.com/updated-webhook"},
        updated_at="2023-01-01T12:00:00Z",
        updated_by="test-user",
    )
    return mock_client


@pytest.mark.asyncio
async def test_update_action_tool_metadata(mock_client_with_update_action):
    """Test the UpdateActionTool's metadata."""
    tool = UpdateActionTool(mock_client_with_update_action)
    
    # Test tool metadata
    assert tool.name == "update_action"
    assert "update" in tool.description.lower()
    assert "action" in tool.description.lower()
    assert tool.annotations.title == "Update Action"
    assert tool.annotations.read_only_hint is False
    assert tool.annotations.destructive_hint is True
    assert tool.annotations.idempotent_hint is False
    assert tool.annotations.open_world_hint is True


@pytest.mark.asyncio
async def test_update_action_tool_execution(mock_client_with_update_action):
    """Test the UpdateActionTool's function execution."""
    tool = UpdateActionTool(mock_client_with_update_action)
    
    # Test input schema
    input_data = {
        "action_identifier": "test-action",
        "identifier": "test-action",
        "title": "Updated Test Action",
        "description": "Updated test action description",
        "trigger": {
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/updated-webhook"},
    }
    
    # Test function execution
    result = await tool.update_action(tool.validate_input(input_data))
    
    # Verify client method was called with correct data
    mock_client_with_update_action.update_action.assert_awaited_once()
    call_args = mock_client_with_update_action.update_action.call_args
    assert call_args[0][0] == "test-action"  # action_identifier
    
    update_data = call_args[0][1]  # action_data
    assert update_data["identifier"] == "test-action"
    assert update_data["title"] == "Updated Test Action"
    assert update_data["description"] == "Updated test action description"
    assert "action_identifier" not in update_data  # Should be removed from update data
    
    # Verify result
    assert result is not None
    assert result["identifier"] == "test-action"
    assert result["title"] == "Updated Test Action"
    assert result["description"] == "Updated test action description"
    assert "updated_at" in result


@pytest.mark.asyncio
async def test_update_action_tool_with_partial_update(mock_client_with_update_action):
    """Test updating an action with partial data."""
    tool = UpdateActionTool(mock_client_with_update_action)
    
    # Mock return value for partial update
    mock_client_with_update_action.update_action.return_value = Action(
        identifier="partial-action",
        title="Partially Updated Action",
        trigger={"type": "self-service"},
        invocationMethod={"type": "WEBHOOK", "url": "https://example.com/webhook"},
        updated_at="2023-01-01T12:00:00Z",
    )
    
    input_data = {
        "action_identifier": "partial-action",
        "identifier": "partial-action",
        "title": "Partially Updated Action",
        "trigger": {"type": "self-service"},
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
    }
    
    result = await tool.update_action(tool.validate_input(input_data))
    
    # Verify client was called
    call_args = mock_client_with_update_action.update_action.call_args
    assert call_args[0][0] == "partial-action"
    
    update_data = call_args[0][1]
    assert update_data["title"] == "Partially Updated Action"
    assert "description" not in update_data  # Not provided in input
    
    # Verify result
    assert result["identifier"] == "partial-action"
    assert result["title"] == "Partially Updated Action"


@pytest.mark.asyncio
async def test_update_action_tool_with_gitlab_invocation(mock_client_with_update_action):
    """Test updating an action with GitLab invocation method."""
    tool = UpdateActionTool(mock_client_with_update_action)
    
    # Mock return value with GitLab invocation
    mock_client_with_update_action.update_action.return_value = Action(
        identifier="gitlab-action",
        title="GitLab Action",
        description="Action with GitLab invocation",
        trigger={
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        invocationMethod={
            "type": "GITLAB",
            "projectName": "test-project",
            "groupName": "test-group",
            "agent": True,
        },
    )
    
    input_data = {
        "action_identifier": "gitlab-action",
        "identifier": "gitlab-action",
        "title": "GitLab Action",
        "description": "Action with GitLab invocation",
        "trigger": {
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        "invocationMethod": {
            "type": "GITLAB",
            "projectName": "test-project",
            "groupName": "test-group",
            "agent": True,
        },
    }
    
    result = await tool.update_action(tool.validate_input(input_data))
    
    assert result["identifier"] == "gitlab-action"
    assert result["invocationMethod"]["type"] == "GITLAB"
    assert result["invocationMethod"]["projectName"] == "test-project"
    assert result["invocationMethod"]["groupName"] == "test-group"
    assert result["invocationMethod"]["agent"] is True


@pytest.mark.asyncio
async def test_update_action_tool_missing_identifier():
    """Test that UpdateActionTool raises ValueError when action_identifier is missing."""
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    
    tool = UpdateActionTool(mock_client)
    
    # Test with empty identifier
    input_data = {
        "action_identifier": "",
        "identifier": "test-action",
        "title": "Test Action",
        "trigger": {"type": "self-service"},
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
    }
    
    with pytest.raises(ValueError, match="Action identifier is required"):
        await tool.update_action(tool.validate_input(input_data))
    
    # Verify client method was not called
    mock_client.update_action.assert_not_called()


@pytest.mark.asyncio
async def test_update_action_tool_none_identifier():
    """Test that UpdateActionTool raises ValueError when action_identifier is None."""
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    
    tool = UpdateActionTool(mock_client)
    
    # Test with None identifier (simulate model_dump returning None)
    from unittest.mock import patch
    with patch.object(tool, 'validate_input') as mock_validate:
        mock_validate.return_value.model_dump.return_value = {
            "action_identifier": None,
            "identifier": "test-action",
            "title": "Test Action",
            "trigger": {"type": "self-service"},
            "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
        }
        
        with pytest.raises(ValueError, match="Action identifier is required"):
            await tool.update_action(mock_validate.return_value)
    
    # Verify client method was not called
    mock_client.update_action.assert_not_called()


@pytest.mark.asyncio
async def test_update_action_tool_complex_trigger_update(mock_client_with_update_action):
    """Test updating an action with complex trigger configuration."""
    tool = UpdateActionTool(mock_client_with_update_action)
    
    # Mock return value with complex trigger
    mock_client_with_update_action.update_action.return_value = Action(
        identifier="complex-action",
        title="Complex Updated Action",
        trigger={
            "type": "automation",
            "event": "entity.created",
            "blueprintIdentifier": "service",
            "condition": {"property": "status", "operator": "=", "value": "active"},
            "userInputs": {
                "properties": {
                    "environment": {"type": "string", "enum": ["dev", "staging", "prod"]},
                    "replicas": {"type": "number", "minimum": 1, "maximum": 10},
                },
                "required": ["environment"],
            },
        },
        invocationMethod={"type": "WEBHOOK", "url": "https://example.com/webhook"},
    )
    
    input_data = {
        "action_identifier": "complex-action",
        "identifier": "complex-action",
        "title": "Complex Updated Action",
        "trigger": {
            "type": "automation",
            "event": "entity.created",
            "blueprintIdentifier": "service",
            "condition": {"property": "status", "operator": "=", "value": "active"},
            "userInputs": {
                "properties": {
                    "environment": {"type": "string", "enum": ["dev", "staging", "prod"]},
                    "replicas": {"type": "number", "minimum": 1, "maximum": 10},
                },
                "required": ["environment"],
            },
        },
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
    }
    
    result = await tool.update_action(tool.validate_input(input_data))
    
    assert result["identifier"] == "complex-action"
    assert result["trigger"]["type"] == "automation"
    assert result["trigger"]["event"] == "entity.created"
    assert result["trigger"]["blueprintIdentifier"] == "service"
    assert "condition" in result["trigger"]
    assert "userInputs" in result["trigger"]
    assert len(result["trigger"]["userInputs"]["required"]) == 1


@pytest.mark.asyncio
async def test_update_action_tool_schema_validation():
    """Test that the UpdateActionTool properly validates input schema."""
    from unittest.mock import MagicMock
    mock_client = MagicMock()
    
    tool = UpdateActionTool(mock_client)
    
    # Test with valid input
    valid_input = {
        "action_identifier": "valid-action",
        "identifier": "valid-action",
        "title": "Valid Action",
        "trigger": {"type": "self-service"},
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
    }
    validated = tool.validate_input(valid_input)
    assert validated.action_identifier == "valid-action"
    assert validated.identifier == "valid-action"
    assert validated.title == "Valid Action"
    
    # Test with invalid input (missing required field action_identifier)
    with pytest.raises(Exception):  # Should raise validation error
        tool.validate_input({
            "identifier": "invalid-action",
            "title": "Invalid Action",
            "trigger": {"type": "self-service"},
            "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
        })
    
    # Test with extra fields (should be ignored)
    extra_input = {
        "action_identifier": "valid-action",
        "identifier": "valid-action",
        "title": "Valid Action",
        "trigger": {"type": "self-service"},
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
        "extra_field": "should_be_ignored"
    }
    validated = tool.validate_input(extra_input)
    assert validated.action_identifier == "valid-action"
    assert not hasattr(validated, "extra_field") 