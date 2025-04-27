from unittest.mock import MagicMock

import pytest

from src.models.tools import ToolMap

from .conftest import TestBaseTool


@pytest.fixture
def clean_tool_map():
    """Fixture to provide a clean ToolMap instance for each test."""
    tool_map = ToolMap(port_client=MagicMock())
    # Store the original tools
    original_tools = tool_map.tools.copy() if hasattr(tool_map, "tools") else {}
    # Clear tools for the test
    if hasattr(tool_map, "tools"):
        tool_map.tools = {}
    yield tool_map
    # Restore original tools after the test
    if hasattr(tool_map, "tools"):
        tool_map.tools = original_tools


@pytest.mark.asyncio
async def test_tool_map_registration_and_lookup(clean_tool_map):
    """Test that ToolMap correctly registers and looks up tools."""
    # Use the clean tool map from the fixture
    tool_map = clean_tool_map

    # Create a test tool
    tool = TestBaseTool()

    # Register the tool
    tool_map.register_tool(tool)

    # Look up the tool
    found_tool = tool_map.get_tool("test_tool")

    # Verify the tool
    assert found_tool is tool

    # Verify looking up a non-existent tool raises an error
    with pytest.raises(ValueError) as excinfo:
        tool_map.get_tool("non_existent_tool")

    # Verify the error
    assert "Tool not found" in str(excinfo.value)

    # Verify listing tools
    tools = tool_map.list_tools()
    assert len(tools) == 1
    assert tools[0].name == "test_tool"
    assert tools[0].description == "A tool for testing"
    # Check that the schema information is included
    assert tools[0].inputSchema is not None
    assert tools[0].annotations is not None


@pytest.mark.asyncio
async def test_tool_map_error_handling(clean_tool_map):
    """Test error handling in ToolMap."""
    # Use the clean tool map from the fixture
    tool_map = clean_tool_map

    # Test looking up a non-existent tool
    with pytest.raises(ValueError) as excinfo:
        tool_map.get_tool("non_existent_tool")
    assert "Tool not found" in str(excinfo.value)

    # Test registering tools with duplicate names
    # First create and register a valid tool
    tool1 = TestBaseTool()
    tool_map.register_tool(tool1)

    # Then create another tool with the same name
    tool2 = TestBaseTool()  # This has the same name "test_tool"

    # Register it - in the current implementation, this will overwrite the first tool
    # Note: We're not testing for an error here since the current implementation allows overwriting
    tool_map.register_tool(tool2)

    # Verify the second tool replaced the first
    assert tool_map.get_tool("test_tool") is tool2
