"""Tests for permissions tools."""

import pytest
from unittest.mock import AsyncMock

from src.tools.permissions import (
    GetUserPermissionsTool,
    CheckActionPermissionTool,
    GetActionPermissionsTool,
)


@pytest.fixture
def mock_client_with_permissions(mock_client):
    """Add specific return values for permissions tests."""
    mock_permissions_client = AsyncMock()
    mock_permissions_client.get_user_permissions.return_value = [
        "execute:actions:test-action",
        "execute:team_entities:actions:team-action",
        "read:entities:Service",
        "write:entities:Service",
    ]
    mock_permissions_client.check_action_permission.return_value = True
    mock_permissions_client.get_action_permissions.return_value = {
        "action_identifier": "test-action",
        "permissions": {"required_permissions": ["execute:actions:test-action"]},
        "approval_config": {"required": False},
        "execution_config": {"timeout": 300},
    }
    
    mock_client.permissions = mock_permissions_client
    return mock_client


@pytest.mark.asyncio
async def test_get_user_permissions_tool(mock_client_with_permissions):
    """Test the GetUserPermissionsTool's metadata and function execution."""
    # Create the tool
    tool = GetUserPermissionsTool(mock_client_with_permissions)

    # Test tool metadata
    assert tool.name == "get_user_permissions"
    assert "permissions" in tool.description.lower()

    # Test function execution
    schema = {}
    result = await tool.get_user_permissions(tool.validate_input(schema))

    # Verify results
    assert "permissions" in result
    assert "total_count" in result
    assert result["total_count"] == 4
    assert "execute:actions:test-action" in result["permissions"]


@pytest.mark.asyncio
async def test_check_action_permission_tool(mock_client_with_permissions):
    """Test the CheckActionPermissionTool's metadata and function execution."""
    # Create the tool
    tool = CheckActionPermissionTool(mock_client_with_permissions)

    # Test tool metadata
    assert tool.name == "check_action_permission"
    assert "permission" in tool.description.lower()

    # Test function execution
    schema = {"action_identifier": "test-action"}
    result = await tool.check_action_permission(tool.validate_input(schema))

    # Verify results
    assert "action_identifier" in result
    assert "has_permission" in result
    assert "permission_types" in result
    assert result["action_identifier"] == "test-action"


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
    assert "action_identifier" in result
    assert "permissions" in result
    assert "approval_config" in result
    assert "execution_config" in result
    assert result["action_identifier"] == "test-action"


@pytest.mark.asyncio
async def test_get_user_permissions_tool_no_permissions_client(mock_client):
    """Test error handling when permissions client is not available."""
    mock_client.permissions = None
    tool = GetUserPermissionsTool(mock_client)

    schema = {}
    with pytest.raises(ValueError, match="Permissions client not available"):
        await tool.get_user_permissions(tool.validate_input(schema))


@pytest.mark.asyncio
async def test_check_action_permission_tool_no_permissions_client(mock_client):
    """Test error handling when permissions client is not available."""
    mock_client.permissions = None
    tool = CheckActionPermissionTool(mock_client)

    schema = {"action_identifier": "test-action"}
    with pytest.raises(ValueError, match="Permissions client not available"):
        await tool.check_action_permission(tool.validate_input(schema))