import asyncio
import pytest
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
import json

# Add src to path
sys.path.append('src')

from src.mcp_server_port.server import main
from src.mcp_server_port.client.client import PortClient


@pytest.fixture
def mock_port_client():
    """Create a mock Port client."""
    client = MagicMock(spec=PortClient)
    client.blueprints = AsyncMock()
    client.entities = AsyncMock()
    client.scorecards = AsyncMock()
    client.agent = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_call_tool_success(mock_port_client):
    """Test that call_tool successfully calls a tool."""
    with patch('src.mcp_server_port.server.PortClient', return_value=mock_port_client):
        with patch('src.mcp_server_port.server.Server') as mock_server:
            # Setup the mock server
            mcp_instance = MagicMock()
            mock_server.return_value = mcp_instance
            
            # Mock the anyio.run to intercept the server startup
            with patch('src.mcp_server_port.server.anyio.run') as mock_run:
                # Call main function
                with patch.dict(os.environ, {"PORT_CLIENT_ID": "test_id", "PORT_CLIENT_SECRET": "test_secret"}):
                    try:
                        main(debug=True)
                    except SystemExit:
                        pass
                    
                    # Verify the Server was initialized
                    mock_server.assert_called_once_with("Port")
                    
                    # Verify call_tool was registered
                    assert mcp_instance.call_tool.called
                    
                    # Get the registered call_tool function
                    call_tool_decorator = mcp_instance.call_tool
                    call_tool_fn = call_tool_decorator.call_args[0][0]
                    
                    # Create a test tool that will be called
                    test_tool = AsyncMock()
                    test_tool.validate_input.return_value = {"param": "value"}
                    test_tool.function.return_value = {"result": "success"}
                    
                    # Mock the tool_map to return our test tool
                    with patch('src.mcp_server_port.server.ToolMap') as mock_tool_map:
                        tool_map_instance = MagicMock()
                        mock_tool_map.return_value = tool_map_instance
                        tool_map_instance.get_tool.return_value = test_tool
                        
                        # Call the function directly
                        result = await call_tool_fn("test_tool", {"param": "value"})
                        
                        # Verify the tool was called correctly
                        tool_map_instance.get_tool.assert_called_once_with("test_tool")
                        test_tool.validate_input.assert_called_once_with({"param": "value"})
                        test_tool.function.assert_called_once_with({"param": "value"})
                        
                        # Verify the result
                        assert result[0].type == "text"
                        assert json.loads(result[0].text) == {"result": "success"}


@pytest.mark.asyncio
async def test_list_tools(mock_port_client):
    """Test that list_tools returns the correct tools."""
    with patch('src.mcp_server_port.server.PortClient', return_value=mock_port_client):
        with patch('src.mcp_server_port.server.Server') as mock_server:
            # Setup the mock server
            mcp_instance = MagicMock()
            mock_server.return_value = mcp_instance
            
            # Mock the anyio.run to intercept the server startup
            with patch('src.mcp_server_port.server.anyio.run') as mock_run:
                # Call main function
                with patch.dict(os.environ, {"PORT_CLIENT_ID": "test_id", "PORT_CLIENT_SECRET": "test_secret"}):
                    try:
                        main(debug=True)
                    except SystemExit:
                        pass
                    
                    # Get the registered list_tools function
                    list_tools_decorator = mcp_instance.list_tools
                    list_tools_fn = list_tools_decorator.call_args[0][0]
                    
                    # Create a mock tool_map
                    with patch('src.mcp_server_port.server.ToolMap') as mock_tool_map:
                        tool_map_instance = MagicMock()
                        mock_tool_map.return_value = tool_map_instance
                        mock_tools = [{"name": "test_tool", "description": "Test tool"}]
                        tool_map_instance.list_tools.return_value = mock_tools
                        
                        # Call the function directly
                        result = await list_tools_fn()
                        
                        # Verify the result
                        assert result == mock_tools
                        tool_map_instance.list_tools.assert_called_once()


@pytest.mark.asyncio
async def test_list_resources(mock_port_client):
    """Test that list_resources returns the correct resources."""
    with patch('src.mcp_server_port.server.PortClient', return_value=mock_port_client):
        with patch('src.mcp_server_port.server.Server') as mock_server:
            # Setup the mock server
            mcp_instance = MagicMock()
            mock_server.return_value = mcp_instance
            
            # Mock the anyio.run to intercept the server startup
            with patch('src.mcp_server_port.server.anyio.run') as mock_run:
                # Call main function
                with patch.dict(os.environ, {"PORT_CLIENT_ID": "test_id", "PORT_CLIENT_SECRET": "test_secret"}):
                    try:
                        main(debug=True)
                    except SystemExit:
                        pass
                    
                    # Get the registered list_resources function
                    list_resources_decorator = mcp_instance.list_resources
                    list_resources_fn = list_resources_decorator.call_args[0][0]
                    
                    # Create a mock resource_map
                    with patch('src.mcp_server_port.server.ResourceMap') as mock_resource_map:
                        resource_map_instance = MagicMock()
                        mock_resource_map.return_value = resource_map_instance
                        mock_resources = [{"name": "test_resource", "description": "Test resource"}]
                        resource_map_instance.list_resources.return_value = mock_resources
                        
                        # Call the function directly
                        result = await list_resources_fn()
                        
                        # Verify the result
                        assert result == mock_resources
                        resource_map_instance.list_resources.assert_called_once()


@pytest.mark.asyncio
async def test_main_missing_credentials():
    """Test main function with missing credentials."""
    with patch.dict(os.environ, {"PORT_CLIENT_ID": "", "PORT_CLIENT_SECRET": ""}):
        with pytest.raises(SystemExit) as exit_info:
            main()
        assert exit_info.value.code == 1 