"""Tests for permissions tools."""

import pytest
from unittest.mock import AsyncMock

from src.tools.permissions import (
    GetActionPermissionsTool,
    UpdateActionPoliciesTool,
)


@pytest.fixture
def mock_client_with_permissions(mock_client):
    """Add specific return values for permissions tests."""
    from unittest.mock import Mock
    
    mock_permissions_client = Mock()
    mock_permissions_client.get_action_permissions = AsyncMock(return_value={
        "action_identifier": "test-action",
        "permissions": {"required_permissions": ["execute:actions:test-action"]},
        "approval_config": {"required": False},
        "execution_config": {"timeout": 300},
    })
    mock_permissions_client.update_action_policies = AsyncMock(return_value={
        "action_identifier": "test-action",
        "updated_policies": {"approval_required": True},
        "success": True,
    })
    
    mock_client.permissions = mock_permissions_client
    return mock_client


@pytest.mark.asyncio
async def test_get_action_permissions_tool(mock_client_with_permissions):
    """Test the GetActionPermissionsTool's metadata and function execution."""
    # Create the tool
    tool = GetActionPermissionsTool(mock_client_with_permissions)

    # Test tool metadata
    assert tool.name == "get_action_permissions"
    assert "permissions" in tool.description.lower()

    # Test function execution
    schema = {"action_identifier": "test-action"}
    result = await tool.get_action_permissions(tool.validate_input(schema))

    # Verify results
    assert "permissions" in result
    permissions = result["permissions"]
    assert "action_identifier" in permissions
    assert "permissions" in permissions
    assert "approval_config" in permissions
    assert "execution_config" in permissions
    assert permissions["action_identifier"] == "test-action"

@pytest.mark.asyncio
async def test_update_action_policies_tool(mock_client_with_permissions):
    """Test the UpdateActionPoliciesTool's metadata and function execution."""
    # Create the tool
    tool = UpdateActionPoliciesTool(mock_client_with_permissions)

    # Test tool metadata
    assert tool.name == "update_action_policies"
    assert "policies" in tool.description.lower()

    # Test function execution
    schema = {
        "action_identifier": "test-action",
        "policies": {"approval_required": True}
    }
    result = await tool.update_action_policies(tool.validate_input(schema))

    # Verify results
    assert "action_identifier" in result
    assert "updated_policies" in result
    assert "success" in result
    assert result["action_identifier"] == "test-action"
    assert result["success"] is True


@pytest.mark.asyncio
async def test_update_action_policies_tool_no_permissions_client(mock_client):
    """Test error handling when permissions client is not available."""
    mock_client.permissions = None
    tool = UpdateActionPoliciesTool(mock_client)

    schema = {
        "action_identifier": "test-action", 
        "policies": {"approval_required": True}
    }
    with pytest.raises(ValueError, match="Permissions client not available"):
        await tool.update_action_policies(tool.validate_input(schema))