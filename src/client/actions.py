from pyport import PortClient

from src.config import config
from src.models.actions import Action
from src.utils import logger


class PortActionClient:
    def __init__(self, client: PortClient):
        self._client = client

    async def get_all_actions(self, trigger_type: str = "self-service") -> list[Action]:
        logger.info("Getting all actions")

        response = self._client.make_request("GET", f"actions?trigger_type={trigger_type}")
        result = response.json().get("actions", [])

        if config.api_validation_enabled:
            logger.debug("Validating actions")
            return [Action(**action) for action in result]
        else:
            logger.debug("Skipping API validation for actions")
            return [Action.construct(**action) for action in result]

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
