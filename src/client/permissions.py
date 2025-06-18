"""Client for Port permissions and RBAC operations."""

from typing import Any

from pyport import PortClient

from src.utils import logger
class PortPermissionsClient:
    """Client for managing Port permissions and RBAC."""

    def __init__(self, client: PortClient):
        self._client = client

    async def get_action_permissions(self, action_identifier: str) -> dict[str, Any]:
        """Get permissions configuration for a specific action."""
        logger.info(f"Getting permissions for action: {action_identifier}")
        
        try:
            response = self._client.make_request("GET", f"v1/actions/{action_identifier}/permissions")
            result = response.json()
            
            if result.get("ok"):
                # The permissions endpoint returns the permissions data directly
                permissions_info = {
                    "action_identifier": action_identifier,
                    "permissions": result.get("permissions", {}),
                    "approval_config": result.get("approval_config", {}),
                    "execution_config": result.get("execution_config", {}),
                }
                logger.debug(f"Retrieved action permissions: {permissions_info}")
                return permissions_info
            else:
                logger.warning(f"Failed to get action permissions: {result}")
                return {}
        except Exception as e:
            logger.error(f"Error getting action permissions: {e}")
            return {}

    async def update_action_policies(self, action_identifier: str, policies: dict[str, Any]) -> dict[str, Any]:
        """Update policies configuration for a specific action."""
        logger.info(f"Updating policies for action: {action_identifier}")
        
        try:
            # Prepare the payload for updating policies - the policies should be sent directly
            payload = policies
            
            response = self._client.make_request("PATCH", f"v1/actions/{action_identifier}/permissions", json=payload)
            result = response.json()
            
            if result.get("ok"):
                # The permissions endpoint returns the updated permissions directly
                updated_info = {
                    "action_identifier": action_identifier,
                    "updated_policies": result.get("permissions", {}),
                    "success": True,
                }
                logger.info(f"Successfully updated policies for action: {action_identifier}")
                return updated_info
            else:
                logger.warning(f"Failed to update action policies: {result}")
                return {
                    "action_identifier": action_identifier,
                    "updated_policies": {},
                    "success": False,
                    "error": result.get("message", "Unknown error"),
                }
        except Exception as e:
            logger.error(f"Error updating action policies: {e}")
            return {
                "action_identifier": action_identifier,
                "updated_policies": {},
                "success": False,
                "error": str(e),
            }