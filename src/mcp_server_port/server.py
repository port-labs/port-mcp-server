#!/usr/bin/env python3

import asyncio
import sys
import os

from mcp.server.fastmcp import FastMCP
from .client import PortClient
from .utils import setup_logging

# Initialize logging
logger = setup_logging()

# Initialize FastMCP server
mcp = FastMCP("Port")

# Initialize Port.io client
port_client = None

@mcp.tool()
async def trigger_port_agent(prompt: str) -> str:
    """Trigger the Port.io AI agent with a prompt and wait for completion."""
    try:
        # Trigger agent
        logger.info(f"Triggering Port.io agent with prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
        response = await port_client.trigger_agent(prompt)
        
        # Get identifier from response
        identifier = response.get("invocation", {}).get("identifier")
        
        if not identifier:
            logger.warning("Could not get invocation identifier from response")
            logger.warning(f"Response data: {response}")
            return "❌ Error: Could not get invocation identifier from response"
        
        logger.info(f"Got invocation identifier: {identifier}")
        
        # Poll for completion
        max_attempts = 10
        attempt = 1
        while attempt < max_attempts:
            logger.info(f"Polling attempt {attempt}/{max_attempts} for invocation {identifier}")
            status = await port_client.get_invocation_status(identifier)
            logger.info(f"Status received: {status.status}")
            
            if status.status.lower() in ["completed", "failed", "error"]:
                logger.info(f"Invocation {identifier} finished with status: {status.status}")
                return status.to_text()
                
            logger.warning(f"Invocation {identifier} still in progress after {attempt * 5} seconds. Status: {status.status}")
            logger.warning(f"Status details: {status.__dict__ if hasattr(status, '__dict__') else status}")
            
            await asyncio.sleep(5)
            attempt += 1
        
        logger.warning(f"Invocation {identifier} timed out after {max_attempts * 5} seconds")
        logger.warning(f"Last status: {status.status}")
        logger.warning(f"Last status details: {status.__dict__ if hasattr(status, '__dict__') else status}")
        
        return f"⏳ Operation timed out. You can check the status later with identifier: {identifier}"
    except Exception as e:
        logger.error(f"Error in trigger_port_agent: {str(e)}", exc_info=True)
        return f"❌ Error: {str(e)}"

def main(client_id=None, client_secret=None, region="EU", **kwargs):
    """
    Main entry point.
    
    Args:
        client_id (str, optional): Port.io client ID
        client_secret (str, optional): Port.io client secret
        region (str, optional): Port.io API region (EU or US)
    """
    global port_client
    
    try:
        logger.info("Starting Port MCP server...")
        
        # Get credentials from environment variables if not provided
        if not client_id:
            client_id = os.environ.get("PORT_CLIENT_ID")
        if not client_secret:
            client_secret = os.environ.get("PORT_CLIENT_SECRET")
        
        # Debug logging
        logger.info(f"Initializing Port.io client with:")
        logger.info(f"  CLIENT_ID: {client_id}")
        logger.info(f"  CLIENT_SECRET: {client_secret[:5]}...{client_secret[-5:] if client_secret else ''}")
        logger.info(f"  REGION: {region}")
        
        if not client_id or not client_secret:
            logger.error("Missing Port.io credentials")
            print("Error: Missing Port.io credentials. Please provide client_id and client_secret as arguments or "
                  "set PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables.", file=sys.stderr)
            sys.exit(1)
            
        # Initialize Port.io client
        port_client = PortClient(client_id=client_id, client_secret=client_secret, region=region)
        
        # Run the server
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
