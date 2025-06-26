import pytest

from src.models.actions import Action
from src.tools.action import CreateActionTool


@pytest.fixture
def mock_client_with_create_action(mock_client):
    """Add specific return values for create action test"""
    from src.models.actions.action import ActionTrigger, ActionInvocationMethodWebhook
    mock_client.create_action.return_value = Action(
        identifier="test-action",
        title="Test Action",
        description="Test action description",
        trigger=ActionTrigger(
            type="self-service",
            operation="CREATE",
            user_inputs={"properties": {}, "required": []},
        ),
        invocation_method=ActionInvocationMethodWebhook(type="WEBHOOK", url="https://example.com/webhook"),
        created_at="2023-01-01T00:00:00Z",
        created_by="test-user",
    )
    return mock_client


@pytest.mark.asyncio
async def test_create_action_tool_metadata(mock_client_with_create_action):
    """Test the CreateActionTool's metadata."""
    tool = CreateActionTool(mock_client_with_create_action)
    
    # Test tool metadata
    assert tool.name == "create_action"
    assert "create" in tool.description.lower()
    assert "action" in tool.description.lower()
    assert tool.annotations.title == "Create Action"
    assert tool.annotations.read_only_hint is False
    assert tool.annotations.destructive_hint is False
    assert tool.annotations.idempotent_hint is False
    assert tool.annotations.open_world_hint is True


@pytest.mark.asyncio
async def test_create_action_tool_execution(mock_client_with_create_action):
    """Test the CreateActionTool's function execution."""
    tool = CreateActionTool(mock_client_with_create_action)
    
    # Test input schema
    input_data = {
        "identifier": "test-action",
        "title": "Test Action",
        "description": "Test action description",
        "trigger": {
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
    }
    
    # Test function execution
    result = await tool.create_action(tool.validate_input(input_data))
    
    # Verify client method was called with correct data
    mock_client_with_create_action.create_action.assert_awaited_once()
    call_args = mock_client_with_create_action.create_action.call_args[0][0]
    assert call_args["identifier"] == "test-action"
    assert call_args["title"] == "Test Action"
    assert call_args["description"] == "Test action description"
    
    # Verify result
    assert result is not None
    assert result["identifier"] == "test-action"
    assert result["title"] == "Test Action"
    assert result["description"] == "Test action description"
    assert "created_at" in result


@pytest.mark.asyncio
async def test_create_action_tool_with_github_invocation(mock_client_with_create_action):
    """Test creating an action with GitHub invocation method."""
    from src.models.actions.action import ActionTrigger, ActionInvocationMethodGitHub
    tool = CreateActionTool(mock_client_with_create_action)
    
    # Mock return value with GitHub invocation
    mock_client_with_create_action.create_action.return_value = Action(
        identifier="github-action",
        title="GitHub Action",
        description="Action with GitHub invocation",
        trigger=ActionTrigger(
            type="self-service",
            operation="CREATE",
            user_inputs={"properties": {}, "required": []},
        ),
        invocation_method=ActionInvocationMethodGitHub(
            type="GITHUB",
            org="test-org",
            repo="test-repo",
            workflow="test-workflow.yml",
        ),
    )
    
    input_data = {
        "identifier": "github-action",
        "title": "GitHub Action",
        "description": "Action with GitHub invocation",
        "trigger": {
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        "invocationMethod": {
            "type": "GITHUB",
            "org": "test-org",
            "repo": "test-repo",
            "workflow": "test-workflow.yml",
        },
    }
    
    result = await tool.create_action(tool.validate_input(input_data))
    
    # Verify the GitHub-specific fields
    assert result["identifier"] == "github-action"
    assert result["invocationMethod"]["type"] == "GITHUB"
    assert result["invocationMethod"]["org"] == "test-org"
    assert result["invocationMethod"]["repo"] == "test-repo"
    assert result["invocationMethod"]["workflow"] == "test-workflow.yml"


@pytest.mark.asyncio
async def test_create_action_tool_with_minimal_data(mock_client_with_create_action):
    """Test creating an action with minimal required data."""
    from src.models.actions.action import ActionTrigger, ActionInvocationMethodWebhook
    tool = CreateActionTool(mock_client_with_create_action)
    
    # Mock return value with minimal data
    mock_client_with_create_action.create_action.return_value = Action(
        identifier="minimal-action",
        title="Minimal Action",
        trigger=ActionTrigger(type="self-service"),
        invocation_method=ActionInvocationMethodWebhook(type="WEBHOOK", url="https://example.com/webhook"),
    )
    
    input_data = {
        "identifier": "minimal-action",
        "title": "Minimal Action",
        "trigger": {"type": "self-service"},
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
    }
    
    result = await tool.create_action(tool.validate_input(input_data))
    
    assert result["identifier"] == "minimal-action"
    assert result["title"] == "Minimal Action"
    assert "description" not in result or result["description"] is None


@pytest.mark.asyncio
async def test_create_action_tool_with_complex_trigger(mock_client_with_create_action):
    """Test creating an action with complex trigger configuration."""
    tool = CreateActionTool(mock_client_with_create_action)
    
    # Mock return value with complex trigger
    mock_client_with_create_action.create_action.return_value = Action(
        identifier="complex-action",
        title="Complex Action",
        trigger={
            "type": "self-service",
            "operation": "DAY-2",
            "blueprintIdentifier": "service",
            "userInputs": {
                "properties": {
                    "name": {"type": "string", "title": "Service Name"},
                    "environment": {"type": "string", "enum": ["dev", "staging", "prod"]},
                },
                "required": ["name", "environment"],
            },
        },
        invocationMethod={"type": "WEBHOOK", "url": "https://example.com/webhook"},
    )
    
    input_data = {
        "identifier": "complex-action",
        "title": "Complex Action",
        "trigger": {
            "type": "self-service",
            "operation": "DAY-2",
            "blueprintIdentifier": "service",
            "userInputs": {
                "properties": {
                    "name": {"type": "string", "title": "Service Name"},
                    "environment": {"type": "string", "enum": ["dev", "staging", "prod"]},
                },
                "required": ["name", "environment"],
            },
        },
        "invocationMethod": {"type": "WEBHOOK", "url": "https://example.com/webhook"},
    }
    
    result = await tool.create_action(tool.validate_input(input_data))
    
    assert result["identifier"] == "complex-action"
    assert result["trigger"]["operation"] == "DAY-2"
    assert result["trigger"]["blueprintIdentifier"] == "service"
    assert "userInputs" in result["trigger"]
    assert len(result["trigger"]["userInputs"]["required"]) == 2


@pytest.mark.asyncio
async def test_create_action_tool_with_string_invocation_method(mock_client_with_create_action):
    """Test creating an action when invocationMethod is provided as a JSON string."""
    from src.models.actions.action import ActionTrigger, ActionInvocationMethodWebhook
    tool = CreateActionTool(mock_client_with_create_action)
    
    # Mock return value with webhook invocation
    mock_client_with_create_action.create_action.return_value = Action(
        identifier="string-invocation-action",
        title="String Invocation Action",
        description="Action with string invocation method",
        trigger=ActionTrigger(
            type="self-service",
            operation="CREATE",
            user_inputs={"properties": {}, "required": []},
        ),
        invocation_method=ActionInvocationMethodWebhook(
            type="WEBHOOK", 
            url="https://api.github.com/repos/test/test/issues",
            method="POST",
            headers={"Accept": "application/vnd.github+json"},
            body={"title": "{{ .inputs.title }}", "body": "{{ .inputs.body }}"}
        ),
    )
    
    # Input data with invocationMethod as a JSON string (like Claude might provide)
    input_data = {
        "identifier": "string-invocation-action",
        "title": "String Invocation Action", 
        "description": "Action with string invocation method",
        "trigger": {
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        "invocationMethod": '{"type": "WEBHOOK", "url": "https://api.github.com/repos/test/test/issues", "method": "POST", "headers": {"Accept": "application/vnd.github+json"}, "body": {"title": "{{ .inputs.title }}", "body": "{{ .inputs.body }}"}}'
    }
    
    # This should work after our fix
    result = await tool.create_action(tool.validate_input(input_data))
    
    # Verify the webhook-specific fields
    assert result["identifier"] == "string-invocation-action"
    assert result["invocationMethod"]["type"] == "WEBHOOK"
    assert result["invocationMethod"]["url"] == "https://api.github.com/repos/test/test/issues"
    assert result["invocationMethod"]["method"] == "POST"
    assert result["invocationMethod"]["headers"]["Accept"] == "application/vnd.github+json"


@pytest.mark.asyncio
async def test_create_action_tool_with_string_github_invocation_method(mock_client_with_create_action):
    """Test creating an action when GitHub invocationMethod is provided as a JSON string."""
    from src.models.actions.action import ActionTrigger, ActionInvocationMethodGitHub
    tool = CreateActionTool(mock_client_with_create_action)
    
    # Mock return value with GitHub invocation
    mock_client_with_create_action.create_action.return_value = Action(
        identifier="string-github-action",
        title="String GitHub Action",
        description="Action with string GitHub invocation method",
        trigger=ActionTrigger(
            type="self-service",
            operation="CREATE",
            user_inputs={"properties": {}, "required": []},
        ),
        invocation_method=ActionInvocationMethodGitHub(
            type="GITHUB",
            org="test-org",
            repo="test-repo", 
            workflow="test-workflow.yml"
        ),
    )
    
    # Input data with GitHub invocationMethod as a JSON string
    input_data = {
        "identifier": "string-github-action",
        "title": "String GitHub Action",
        "description": "Action with string GitHub invocation method",
        "trigger": {
            "type": "self-service",
            "operation": "CREATE",
            "userInputs": {"properties": {}, "required": []},
        },
        "invocationMethod": '{"type": "GITHUB", "org": "test-org", "repo": "test-repo", "workflow": "test-workflow.yml"}'
    }
    
    # This should work after our fix
    result = await tool.create_action(tool.validate_input(input_data))
    
    # Verify the GitHub-specific fields
    assert result["identifier"] == "string-github-action"
    assert result["invocationMethod"]["type"] == "GITHUB"
    assert result["invocationMethod"]["org"] == "test-org"
    assert result["invocationMethod"]["repo"] == "test-repo"
    assert result["invocationMethod"]["workflow"] == "test-workflow.yml" 