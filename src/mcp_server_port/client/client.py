import logging
import pyport
from typing import Dict, Any, Optional
from ..models import PortAgentResponse
from ..config import PORT_API_BASE
from ..utils import PortError

logger = logging.getLogger(__name__)

class PortClient:
    """Client for interacting with the Port.io API."""
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, region: str = "EU", base_url: str = PORT_API_BASE):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        
        if not client_id or not client_secret:
            logger.warning("Port.io client initialized without credentials")
            self._client = None
        else:
            self._client = pyport.PortClient(client_id=client_id, client_secret=client_secret, us_region=(region == "US"))

    async def trigger_agent(self, prompt: str) -> Dict[str, Any]:
        """Trigger the Port.io AI agent with a prompt."""
        if not self._client:
            raise PortError("Cannot trigger agent: Port.io client not initialized with credentials")
            
        try:
            endpoint = "agent/invoke"
            data = {"prompt": prompt}
            
            # Use the make_request method directly since custom is not available
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
            raise PortError("Cannot get invocation status: Port.io client not initialized with credentials")
            
        try:
            endpoint = f"agent/invoke/{identifier}"
            
            response = self._client.make_request(
                method="GET",
                endpoint=endpoint
            )
            
            response_data = response.json()
            logger.debug(f"Get invocation response: {response_data}")
            
            # Handle the new response format where data is in result field
            if response_data.get("ok") and "result" in response_data:
                result = response_data["result"]
                status = result.get("status", "Unknown")
                message = result.get("message", "")
                selected_agent = result.get("selectedAgent", "")
                
                # Generate action URL from port URLs in message if present
                action_url = None
                if message:
                    import re
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
            
            # Fallback to old format (entity.properties)
            properties = response_data.get("entity", {}).get("properties", {})
            
            # Extract action URL if present
            output = properties.get("outputMessage") or properties.get("output")
            action_url = None
            
            if output:
                # Look for URLs in the output
                import re
                urls = re.findall(r'https://app\.getport\.io/[^\s<>"]+', output)
                if urls:
                    action_url = urls[0]
            
            return PortAgentResponse(
                identifier=identifier,
                status=properties.get("status", "Unknown"),
                output=output,
                error=properties.get("error"),
                action_url=action_url
            )
        except Exception as e:
            logger.error(f"Error getting invocation status: {str(e)}")
            raise PortError(f"Error getting invocation status: {str(e)}") 