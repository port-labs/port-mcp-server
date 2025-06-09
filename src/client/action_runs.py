from pyport import PortClient

from src.models.action_run import ActionRun
from src.utils import logger


class PortActionRunClient:
    def __init__(self, client: PortClient):
        self._client = client

    async def create_global_action_run(self, action_identifier: str, **kwargs) -> ActionRun:
        logger.info(f"Creating global action run for: {action_identifier}")
        response = self._client.make_request(
            "POST", f"actions/{action_identifier}/runs", json=kwargs
        )
        action_run_data = response.json().get("run", response.json())
        return ActionRun.construct(**action_run_data)

    async def create_entity_action_run(self, action_identifier: str, **kwargs) -> ActionRun:
        logger.info(f"Creating entity action run for {action_identifier} with kwargs: {kwargs}")
        response = self._client.make_request(
            "POST",
            f"actions/{action_identifier}/runs",
            json=kwargs,
        )
        action_run_data = response.json().get("run", response.json())
        return ActionRun.construct(**action_run_data)

    async def get_action_run(self, run_id: str) -> ActionRun:
        logger.debug(f"Getting action run status for: {run_id}")
        response = self._client.make_request("GET", f"actions/runs/{run_id}?version=v2")
        action_run_data = response.json().get("run", response.json())
        return ActionRun.construct(**action_run_data)
