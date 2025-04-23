#!/usr/bin/env python3
from src.server.config import config

import json
import sys
import anyio
from typing import Any
import mcp.types as types
from mcp.server.lowlevel import Server

from src.server.handlers import execute_tool
from src.server.models.tools import ToolMap
from src.server.client import PortClient
from src.server.utils import setup_logging

def main():

    logger = setup_logging()

    try:
        # Set logging level based on debug flag
            
        logger.info("Starting Port MCP server...")
        
        # Initialize Port.io client
        port_client = PortClient(client_id=config.port_client_id, client_secret=config.port_client_secret, region=config.region)
        
        # Initialize FastMCP server
        mcp = Server("Port MCP Server")

        tool_map = ToolMap(port_client=port_client)

        @mcp.call_tool()
        async def call_tool(tool_name: str, arguments:dict[str, Any]):
            tool = tool_map.get_tool(tool_name)
            logger.debug(f"Calling tool: {tool_name} with arguments: {arguments}")
            return await execute_tool(tool, arguments)
        
        @mcp.list_tools()
        async def list_tools() -> list[types.Tool]:
            return tool_map.list_tools()

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
