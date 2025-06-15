from pyport import PortClient

from src.config import config
from src.models.actions import Action
from src.utils import logger


class PortActionClient:
    def __init__(self, client: PortClient):
        self._client = client

    async def _get_user_permissions(self) -> list[str]:
        """Get user permissions from auth endpoint"""
        logger.info("Getting user permissions")

        response = self._client.make_request("GET", "auth/permissions?action_version=v2")
        result = response.json()
        if result.get("ok"):
            permissions = result.get("permissions", [])
            logger.debug(f"listed permissions: {permissions}")
            if not isinstance(permissions, list):
                logger.warning("Permissions response is not a list")
                return []
            return permissions
        else:
            logger.warning("Failed to get user permissions")
            return []

    def _has_action_permission(self, action_identifier: str, permissions: list[str]) -> bool:
        """Check if user has permission to execute the action"""
        execute_action_permission = f"execute:actions:{action_identifier}"
        team_execute_permission = f"execute:team_entities:actions:{action_identifier}"

        return execute_action_permission in permissions or team_execute_permission in permissions

    async def get_all_actions(self, trigger_type: str = "self-service") -> list[Action]:
        logger.info("Getting all actions")

        response = self._client.make_request("GET", f"actions?trigger_type={trigger_type}")
        result = response.json().get("actions", [])

        user_permissions = await self._get_user_permissions()

        filtered_actions = []
        for action_data in result:
            action_identifier = action_data.get("identifier")
            if self._has_action_permission(action_identifier, user_permissions):
                filtered_actions.append(action_data)
            else:
                logger.debug(f"User lacks permission for action: {action_identifier}")

        if config.api_validation_enabled:
            logger.debug("Validating actions")
            return [Action(**action) for action in filtered_actions]
        else:
            logger.debug("Skipping API validation for actions")
            return [Action.construct(**action) for action in filtered_actions]

    async def get_action(self, action_identifier: str) -> Action:
        logger.info(f"Getting action: {action_identifier}")

        response = self._client.make_request("GET", f"actions/{action_identifier}")
        result = response.json().get("action")

        if config.api_validation_enabled:
            logger.debug("Validating action")
            return Action(**result)
        else:
            logger.debug("Skipping API validation for action")
            return Action.construct(**result)
