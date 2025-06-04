from typing import Any, Dict, List

import pyport

from src.utils import logger


class PortActionRunClient:
    """Client for Port action runs."""

    def __init__(self, client: pyport.PortClient):
        self.client = client

    async def create_global_action_run(self, action_identifier: str, **kwargs) -> Dict[str, Any]:
        """Create a global action run."""
        logger.info(f"Creating global action run for: {action_identifier}")
        return await self.client.action_runs.create_global_action_run(action_identifier, **kwargs)

    async def create_blueprint_action_run(self, blueprint_identifier: str, action_identifier: str, **kwargs) -> Dict[str, Any]:
        """Create a blueprint action run."""
        logger.info(f"Creating blueprint action run for {blueprint_identifier}.{action_identifier}")
        return await self.client.action_runs.create_blueprint_action_run(blueprint_identifier, action_identifier, **kwargs)

    async def create_entity_action_run(
        self, blueprint_identifier: str, entity_identifier: str, action_identifier: str, **kwargs
    ) -> Dict[str, Any]:
        """Create an entity action run."""
        logger.info(f"Creating entity action run for {blueprint_identifier}.{entity_identifier}.{action_identifier}")
        return await self.client.action_runs.create_entity_action_run(
            blueprint_identifier, entity_identifier, action_identifier, **kwargs
        )

    async def get_action_run(self, run_id: str) -> Dict[str, Any]:
        """Get action run status and details."""
        logger.debug(f"Getting action run status for: {run_id}")
        return await self.client.action_runs.get_action_run(run_id)

    async def get_action_run_logs(self, run_id: str) -> List[Dict[str, Any]]:
        """Get action run logs."""
        logger.debug(f"Getting action run logs for: {run_id}")
        return await self.client.action_runs.get_action_run_logs(run_id) 