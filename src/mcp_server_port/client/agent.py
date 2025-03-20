import logging
from typing import Dict, Any
import re
from ..models.models import PortAgentResponse
from ..utils import PortError

logger = logging.getLogger(__name__)

class PortAgentClient:
    """Client for interacting with Port AI Agent APIs."""
    
    def __init__(self, client):
        self._client = client

    async def trigger_agent(self, prompt: str) -> Dict[str, Any]:
        """Trigger the Port AI agent with a prompt."""
        if not self._client:
            raise PortError("Cannot trigger agent: Port client not initialized with credentials")
            
        try:
            endpoint = "agent/invoke"
            data = {"prompt": prompt}
            
            response = self._client.make_request(
                method="POST",
                endpoint=endpoint,
                json=data
            )
            
            response_data = response.json()
            
            # Check for nested identifier in invocation object
            if response_data.get("ok") and response_data.get("invocation", {}).get("identifier"):
                return response_data
            
            # Fallback to direct identifier fields
            identifier = response_data.get("identifier") or response_data.get("id") or response_data.get("invocationId")
            if not identifier:
                logger.error("Response missing identifier")
                raise PortError("Response missing identifier")
            return response_data
        except Exception as e:
            logger.error(f"Error in trigger_agent: {str(e)}")
            raise
    
    async def get_invocation_status(self, identifier: str) -> PortAgentResponse:
        """Get the status of an AI agent invocation."""
        if not self._client:
            raise PortError("Cannot get invocation status: Port client not initialized with credentials")
            
        try:
            endpoint = f"agent/invoke/{identifier}"
            
            response = self._client.make_request(
                method="GET",
                endpoint=endpoint
            )
            
            response_data = response.json()
            logger.debug(f"Get invocation response: {response_data}")
            
            # Response format with data in result field
            if response_data.get("ok") and "result" in response_data:
                result = response_data["result"]
                status = result.get("status", "Unknown")
                message = result.get("message", "")
                
                # Generate action URL from port URLs in message if present
                action_url = None
                if message:
                    urls = re.findall(r'https://app\.getport\.io/self-serve[^\s<>"]*', message)
                    if urls:
                        action_url = urls[0]
                
                return PortAgentResponse(
                    identifier=identifier,
                    status=status,
                    output=message,
                    error=None if status.lower() != "error" else message,
                    action_url=action_url
                )
            
            # If we don't have a result field, raise an error
            logger.error(f"Invalid response format: {response_data}")
            raise PortError(f"Invalid response format: {response_data}")
            
        except Exception as e:
            logger.error(f"Error getting invocation status: {str(e)}")
            raise PortError(f"Error getting invocation status: {str(e)}")