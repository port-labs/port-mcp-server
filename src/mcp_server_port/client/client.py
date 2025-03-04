import httpx
import logging
from typing import Dict, Optional, Any
from ..models import PortToken, PortAgentResponse
from ..config import PORT_API_BASE
from ..utils import PortError, PortAuthError

logger = logging.getLogger(__name__)

class PortClient:
    """Client for interacting with the Port.io API."""
    
    def __init__(self, base_url: str = PORT_API_BASE):
        self.base_url = base_url
        self._client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()
    
    async def _make_request(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a request to the Port.io API with proper error handling."""
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        
        try:
            if method == "GET":
                response = await self._client.get(url, headers=headers)
            elif method == "POST":
                response = await self._client.post(url, headers=headers, json=json_data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json()
            except:
                error_detail = e.response.text if e.response.text else str(e)
            
            if e.response.status_code == 401:
                raise PortAuthError(f"Authentication failed: {error_detail}")
            raise PortError(f"Port.io API error (HTTP {e.response.status_code}): {error_detail}")
        except Exception as e:
            raise PortError(f"Error making Port.io request: {str(e)}")
    
    async def get_token(self, client_id: str, client_secret: str) -> PortToken:
        """Get an authentication token using client credentials."""
        url = f"{self.base_url}/auth/access_token"
        data = {
            "clientId": client_id,
            "clientSecret": client_secret
        }
        
        try:
            response = await self._make_request(url, method="POST", json_data=data)
            return PortToken(
                access_token=response["accessToken"],
                expires_in=response["expiresIn"],
                token_type=response["tokenType"]
            )
        except Exception as e:
            logger.error(f"Token request failed: {str(e)}")
            raise
    
    async def trigger_agent(self, token: str, prompt: str) -> Dict[str, Any]:
        """Trigger the Port.io AI agent with a prompt."""
        url = f"{self.base_url}/agent/invoke"
        headers = {"Authorization": f"Bearer {token}"}
        data = {"prompt": prompt}
        
        try:
            response = await self._client.post(url, headers=headers, json=data)
            
            if response.status_code == 202:
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
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error in trigger_agent: {str(e)}")
            raise
    
    async def get_invocation_status(self, token: str, identifier: str) -> PortAgentResponse:
        """Get the status of an AI agent invocation."""
        url = f"{self.base_url}/blueprints/ai_invocations/entities/{identifier}"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self._make_request(url, method="GET", headers=headers)
        
        # Get the properties from the entity
        properties = response.get("entity", {}).get("properties", {})
        
        # Extract action URL and type if present
        output = properties.get("outputMessage") or properties.get("output")
        action_url = None
        action_type = None
        
        if output:
            # Look for URLs in the output
            import re
            urls = re.findall(r'https://app\.getport\.io/[^\s<>"]+', output)
            if urls:
                action_url = urls[0]
                # Determine action type based on URL pattern
                if "jira_bugEntity" in action_url:
                    action_type = "bug_report"
                elif "self-serve" in action_url:
                    action_type = "action"
        
        return PortAgentResponse(
            identifier=identifier,
            status=properties.get("status", "Unknown"),
            output=output,
            error=properties.get("error"),
            action_url=action_url,
            action_type=action_type
        ) 