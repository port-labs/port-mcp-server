#!/usr/bin/env python3

import sys
import os

from mcp.server.fastmcp import FastMCP
from .client import PortClient
from .utils import setup_logging
from .tools.agent_tools import register as register_agent_tools
from .tools.blueprint_tools import register as register_blueprint_tools
from .resources import register_all as register_all_resources
from .prompts import register_all as register_all_prompts

# Initialize logging
logger = setup_logging()

def main(client_id=None, client_secret=None, region="EU", **kwargs):
    """
    Main entry point.
    
    Args:
        client_id (str, optional): Port.io client ID
        client_secret (str, optional): Port.io client secret
        region (str, optional): Port.io API region (EU or US)
    """
    try:
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
        mcp = FastMCP("Port")
        
        # Register tools
        register_agent_tools(mcp, port_client)
        register_blueprint_tools(mcp, port_client)
        
        # Register resources
        register_all_resources(mcp, port_client)
        
        # Register prompts
        register_all_prompts(mcp)
        
        # Run the server
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
