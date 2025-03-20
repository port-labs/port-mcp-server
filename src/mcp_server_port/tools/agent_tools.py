"""Agent-related tools for Port MCP server."""

import asyncio
import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

async def _invoke_ai_agent_internal(
    prompt: str, 
    mcp: FastMCP, 
    port_client: Any
) -> str:
    """
    Invoke the Port's AI agent with a prompt and wait for completion.
    
    Args:
        prompt: The prompt to send to the Port AI agent
        mcp: The FastMCP server instance 
        port_client: The Port client instance
    
    Returns:
        The result of the AI agent invocation
    """
    try:
        # Trigger agent
        logger.info(f"Invoking Port's AI agent with prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
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
        logger.error(f"Error in invoke_ai_agent: {str(e)}", exc_info=True)
        return f"❌ Error: {str(e)}"

def register(mcp: FastMCP, port_client: Any) -> None:
    """
    Register agent tools with the FastMCP server.
    
    Args:
        mcp: The FastMCP server instance
        port_client: The Port client instance
    """
    @mcp.tool()
    async def invoke_ai_agent(prompt: str) -> str:
        """
        Invoke the Port AI agent with a natural language prompt.
        
        Use this to interact with user-defined AI agents in Port for complex queries or actions.
        This tool allows natural language interactions with your Port data and can perform
        queries like "which service has the highest scorecard level" or actions like 
        "report a documentation issue".
        
        Args:
            prompt: The natural language prompt to send to the Port AI agent
        
        Returns:
            The response from the Port AI agent after the operation is complete
        """
        return await _invoke_ai_agent_internal(prompt, mcp, port_client)
