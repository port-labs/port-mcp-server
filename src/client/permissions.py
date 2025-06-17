"""Client for Port permissions and RBAC operations."""

from typing import Any

from pyport import PortClient

from src.utils import logger


class PortPermissionsClient:
    """Client for managing Port permissions and RBAC."""

    def __init__(self, client: PortClient):
        self._client = client

    async def get_user_permissions(self) -> list[str]:
        """Get user permissions from auth endpoint."""
        logger.info("Getting user permissions")

        response = self._client.make_request("GET", "auth/permissions?action_version=v2")
        result = response.json()
        if result.get("ok"):
            permissions = result.get("permissions", [])
            logger.debug(f"Retrieved permissions: {permissions}")
            if not isinstance(permissions, list):
                logger.warning("Permissions response is not a list")
                return []
            return permissions
        else:
            logger.warning("Failed to get user permissions")
            return []

    def check_action_permission(self, action_identifier: str, permissions: list[str]) -> bool:
        """Check if user has permission to execute the action."""
        execute_action_permission = f"execute:actions:{action_identifier}"
        team_execute_permission = f"execute:team_entities:actions:{action_identifier}"

        has_permission = execute_action_permission in permissions or team_execute_permission in permissions
        logger.debug(f"Action permission check for '{action_identifier}': {has_permission}")
        return has_permission

    async def get_action_permissions(self, action_identifier: str) -> dict[str, Any]:
        """Get permissions configuration for a specific action."""
        logger.info(f"Getting permissions for action: {action_identifier}")
        
        try:
            response = self._client.make_request("GET", f"actions/{action_identifier}")
            result = response.json()
            
            if result.get("ok"):
                action_data = result.get("action", {})
                # Extract permissions-related fields from the action
                permissions_info = {
                    "action_identifier": action_identifier,
                    "permissions": action_data.get("permissions", {}),
                    "approval_config": action_data.get("approval_config", {}),
                    "execution_config": action_data.get("execution_config", {}),
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
            # Prepare the payload for updating policies
            payload = {"policies": policies}
            
            response = self._client.make_request("PATCH", f"actions/{action_identifier}", json=payload)
            result = response.json()
            
            if result.get("ok"):
                action_data = result.get("action", {})
                updated_info = {
                    "action_identifier": action_identifier,
                    "updated_policies": action_data.get("policies", {}),
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