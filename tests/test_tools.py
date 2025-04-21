import pytest
import sys
from unittest.mock import AsyncMock, MagicMock, patch
import json

# Add src to path
sys.path.append('src')

from src.mcp_server_port.models.tools.tool_map import ToolMap
from src.mcp_server_port.models.tools.base_tool import BaseTool
from src.mcp_server_port.tools.blueprint import GetBlueprintsTool
from src.mcp_server_port.tools.entity import GetEntityTool


class MockTool(BaseTool):
    """Mock tool for testing."""
    name = "mock_tool"
    description = "A mock tool for testing"
    parameters = {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Test parameter"},
            "param2": {"type": "integer", "description": "Another test parameter"}
        },
        "required": ["param1"]
    }
    
    async def _function(self, args):
        return {"result": f"executed with {args['param1']}"}


@pytest.fixture
def mock_client():
    """Create a mock client."""
    client = MagicMock()
    client.blueprints = AsyncMock()
    client.entities = AsyncMock()
    client.blueprints.get_blueprints.return_value = [{"id": "test-blueprint"}]
    client.entities.get_entity.return_value = {"id": "test-entity"}
    return client


@pytest.fixture
def tool_map():
    """Create a ToolMap instance."""
    return ToolMap()


def test_tool_map_registration(tool_map):
    """Test that tools can be registered with the ToolMap."""
    mock_tool = MockTool(None)
    tool_map.register_tool(mock_tool)
    
    assert "mock_tool" in tool_map.tools
    assert tool_map.tools["mock_tool"] is mock_tool
    
    # Test getting tool
    assert tool_map.get_tool("mock_tool") is mock_tool
    
    # Test getting non-existent tool
    with pytest.raises(ValueError):
        tool_map.get_tool("non_existent_tool")
    
    # Test listing tools
    tools_list = tool_map.list_tools()
    assert len(tools_list) == 1
    assert tools_list[0]["name"] == "mock_tool"
    assert tools_list[0]["description"] == "A mock tool for testing"


@pytest.mark.asyncio
async def test_get_blueprints_tool(mock_client):
    """Test the GetBlueprintsTool."""
    # Create the tool
    tool = GetBlueprintsTool(mock_client)
    
    # Test tool metadata
    assert tool.name == "get_blueprints"
    assert "Get all blueprints" in tool.description
    assert tool.parameters is not None
    
    # Test function execution
    result = await tool.function({})
    mock_client.blueprints.get_blueprints.assert_awaited_once()
    assert result == [{"id": "test-blueprint"}]


@pytest.mark.asyncio
async def test_get_entity_tool(mock_client):
    """Test the GetEntityTool."""
    # Create the tool
    tool = GetEntityTool(mock_client)
    
    # Test tool metadata
    assert tool.name == "get_entity"
    assert "Get an entity" in tool.description.lower()
    assert "blueprint_id" in tool.parameters["properties"]
    assert "entity_id" in tool.parameters["properties"]
    assert "blueprint_id" in tool.parameters["required"]
    assert "entity_id" in tool.parameters["required"]
    
    # Test function execution
    result = await tool.function({"blueprint_id": "test-blueprint", "entity_id": "test-entity"})
    mock_client.entities.get_entity.assert_awaited_once_with("test-blueprint", "test-entity")
    assert result == {"id": "test-entity"}


@pytest.mark.asyncio
async def test_input_validation(mock_client):
    """Test that tool input validation works correctly."""
    # Create a mock tool
    tool = MockTool(mock_client)
    
    # Test with valid input
    valid_args = {"param1": "test", "param2": 42}
    assert tool.validate_input(valid_args) == valid_args
    
    # Test with missing required parameter
    invalid_args = {"param2": 42}
    with pytest.raises(ValueError) as excinfo:
        tool.validate_input(invalid_args)
    assert "param1" in str(excinfo.value)
    
    # Test with wrong type
    wrong_type_args = {"param1": "test", "param2": "not_an_integer"}
    with pytest.raises(ValueError) as excinfo:
        tool.validate_input(wrong_type_args)
    assert "param2" in str(excinfo.value) 