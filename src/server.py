# ruff: noqa: I001

import sys
from typing import Any

import anyio
import mcp.types as types
from mcp.server.lowlevel import Server

from src.handlers import execute_tool
from src.maps.tool_map import tool_map
from src.utils import logger
from src.config import config


def main():
    try:
        # Set logging level based on debug flag

        logger.info("Starting Port MCP server...")
        logger.debug(f"Server config: {config}")
        # Initialize Port.io client

        # Initialize FastMCP server
        mcp: Server = Server("Port MCP Server")

        @mcp.call_tool()
        async def call_tool(tool_name: str, arguments: dict[str, Any]):
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
                await mcp.run(streams[0], streams[1], mcp.create_initialization_options())

        anyio.run(arun)
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.exception(f"Server error: {e}")
        sys.exit(1)
