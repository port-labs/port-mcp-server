import json
from typing import Any

from pyport import PortClient

from src.config import config
from src.models.blueprints import Blueprint
from src.utils import logger
from src.utils.errors import PortError


class PortBlueprintClient:
    """Client for interacting with Port Blueprint APIs."""

    def __init__(self, client: PortClient):
        self._client = client

    async def get_blueprints(self) -> list[Blueprint]:
        logger.info("Getting blueprints from Port")

        blueprints = self._client.blueprints.get_blueprints()

        logger.info("Got blueprints from Port")

        logger.debug(f"Response for get blueprints: {blueprints}")
        if config.api_validation_enabled:
            logger.debug("Validating blueprints")
            return [Blueprint(**bp) for bp in blueprints]
        else:
            logger.debug("Skipping API validation for blueprints")
            return [Blueprint.construct(**bp) for bp in blueprints]

    async def get_blueprint(self, blueprint_identifier: str) -> Blueprint:
        logger.info(f"Getting blueprint '{blueprint_identifier}' from Port")

        bp_data = self._client.blueprints.get_blueprint(blueprint_identifier)

        logger.debug(f"Response for get blueprint: {bp_data}")

        logger.info(f"Got blueprint '{blueprint_identifier}' from Port")

        if config.api_validation_enabled:
            logger.debug("Validating blueprint")
            return Blueprint(**bp_data)
        else:
            logger.debug("Skipping API validation for blueprint")
            return Blueprint.construct(**bp_data)

    async def create_blueprint(self, blueprint_data: dict[str, Any]) -> Blueprint:
        data_json = json.dumps(blueprint_data)

        logger.info("Creating blueprint in Port")
        logger.debug(f"Input from tool to create blueprint: {data_json}")

        response = self._client.make_request("POST", "blueprints", json=blueprint_data)
        result = response.json()
        if not result.get("ok"):
            message = f"Failed to create blueprint: {result}"
            logger.warning(message)
            raise PortError(message)
        logger.info("Blueprint created in Port")

        result = result.get("blueprint", {})

        if config.api_validation_enabled:
            logger.debug("Validating blueprint")
            blueprint = Blueprint(**result)
        else:
            logger.debug("Skipping API validation for blueprint")
            blueprint = Blueprint.construct(**result)
        logger.debug(f"Response for create blueprint: {blueprint}")
        return blueprint

    async def update_blueprint(self, blueprint_data: dict[str, Any]) -> Blueprint:
        data_json = json.dumps(blueprint_data)

        logger.info("Updating blueprint in Port")
        logger.debug(f"Input from tool to update blueprint: {data_json}")

        response = self._client.make_request("PATCH", f"blueprints/{blueprint_data.get('identifier')}", json=blueprint_data)
        result = response.json()
        if not result.get("ok"):
            message = f"Failed to update blueprint: {result}"
            logger.warning(message)
            raise PortError(message)
        logger.info("Blueprint updated in Port")

        result = result.get("blueprint", {})
        if config.api_validation_enabled:
            logger.debug("Validating blueprint")
            blueprint = Blueprint(**result)
        else:
            logger.debug("Skipping API validation for blueprint")
            blueprint = Blueprint.construct(**result)
        logger.debug(f"Response for update blueprint: {blueprint}")
        return blueprint

    async def delete_blueprint(self, blueprint_identifier: str) -> bool:
        logger.info(f"Deleting blueprint '{blueprint_identifier}' from Port")

        response = self._client.make_request("DELETE", f"blueprints/{blueprint_identifier}")
        result = response.json()
        if not result.get("ok"):
            message = f"Failed to delete blueprint: {result}"
            logger.warning(message)
            raise PortError(message)
        logger.info("Blueprint deleted in Port")

        return True
