#!/usr/bin/env python3

import json
import sys
import os
import anyio
from typing import Any
import mcp.types as types
from mcp.server.lowlevel import Server

from src.mcp_server_port.models.resources.resource_map import ResourceMap
from src.mcp_server_port.resources.blueprint.get_blueprint import GetBlueprints
from src.mcp_server_port.models.tools.tool_map import ToolMap
from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.utils.logging import setup_logging
from pydantic import AnyUrl, ValidationError
import src.mcp_server_port.tools as mcp_tools
# Initialize logging
logger = setup_logging()

def main(client_id=None, client_secret=None, region="EU", debug=False, **kwargs):
    """
    Main entry point.
    
    Args:
        client_id (str, optional): Port.io client ID
        client_secret (str, optional): Port.io client secret
        region (str, optional): Port.io API region (EU or US)
        debug (bool, optional): Enable debug output
    """
    try:
        # Set logging level based on debug flag
        if debug:
            logger.level("DEBUG")
            
        logger.info("Starting Port MCP server...")
        
        # Get credentials from environment variables if not provided
        if not client_id:
            client_id = os.environ.get("PORT_CLIENT_ID")
        if not client_secret:
            client_secret = os.environ.get("PORT_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            logger.error("Missing Port.io credentials")
            print("Error: Missing Port.io credentials. Please provide client_id and client_secret as arguments or "
                  "set PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables.", file=sys.stderr)
            sys.exit(1)
            
        # Initialize Port.io client
        port_client = PortClient(client_id=client_id, client_secret=client_secret, region=region)
        
        # Initialize FastMCP server
        log_level = "DEBUG" if debug else "ERROR"
        logger.info(f"Initializing FastMCP server with log_level={log_level}")
        mcp = Server("Port")


        tool_map = ToolMap()
        tools = [mcp_tools.__dict__[tool](port_client) for tool in mcp_tools.__all__]
        for tool in tools:
            tool_map.register_tool(tool)
        resource_map = ResourceMap()
        resources = [GetBlueprints(port_client)]
        for resource in resources:
            resource_map.register_resource(resource)
        
        @mcp.call_tool()
        async def call_tool(tool_name: str, arguments:dict[str, Any]):
            tool = tool_map.get_tool(tool_name)
            #debug
            logger.info(f"Calling tool: {tool_name} with arguments: {arguments}")
            
            try:
                validated_args = tool.validate_input(arguments)
                result = await tool.function(validated_args)
                # debug
                logger.info(f"Tool {tool_name} returned: {result}")
                return [types.TextContent(type="text", text=json.dumps(result))]
            except ValidationError as e:
                errors = e.errors()
                logger.error(f"Error calling tool {tool_name}: {errors}")
                raise Exception(f"Error calling tool {tool_name}: {errors}")
            except Exception as e:
                logger.exception(f"Error calling tool {tool_name}: {e}")
                raise Exception(f"Error calling tool {tool_name}: {e}")
        
        @mcp.list_tools()
        async def list_tools() -> list[types.Tool]:
            """Return a list of available tools, ensuring any Pydantic models are converted to dictionaries"""
            return tool_map.list_tools()

        @mcp.list_resources()  
        async def list_resources() -> list[types.Resource]:
            return resource_map.list_resources()
        
        @mcp.list_resource_templates()
        async def list_resource_templates() -> list[types.ResourceTemplate]:
            logger.info("Listing resource templates")
            return [types.ResourceTemplate(name="blueprints", description="Get blueprint by identifier",uri=AnyUrl('blueprints://{blueprint_id}'),mimeType="text/plain")]
        
        @mcp.read_resource()
        async def read_resource(resource_uri: AnyUrl) -> str:
            logger.info(f"Reading resource: {resource_uri}")
            if resource_uri == "blueprints":
                return await resource_map.get_resource(resource_uri)()
            else:
                raise ValueError(f"Unsupported resource URI: {resource_uri}")
        
        # Run the server
        logger.info("Starting FastMCP server on stdio transport")
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await mcp.run(
                    streams[0], streams[1], mcp.create_initialization_options()
                )

        anyio.run(arun)
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.exception(f"Server error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
