from typing import Any, Dict, List

import pyport

from src.utils import logger


class PortActionClient:
    """Client for Port actions."""

    def __init__(self, client: pyport.PortClient):
        self.client = client

    async def get_all_actions(self) -> List[Dict[str, Any]]:
        """Get all available actions."""
        logger.info("Getting all actions")
        # Use the PyPort actions API - this may need adjustment based on actual PyPort API
        return await self.client.actions.get_all_actions()

    async def get_blueprint_actions(self, blueprint_identifier: str) -> List[Dict[str, Any]]:
        """Get actions for a specific blueprint."""
        logger.info(f"Getting actions for blueprint: {blueprint_identifier}")
        return await self.client.actions.get_blueprint_actions(blueprint_identifier)

    async def get_action(self, action_identifier: str, blueprint_identifier: str = None) -> Dict[str, Any]:
        """Get a specific action."""
        logger.info(f"Getting action: {action_identifier}")
        if blueprint_identifier:
            return await self.client.actions.get_blueprint_action(blueprint_identifier, action_identifier)
        else:
            return await self.client.actions.get_action(action_identifier) 