import json
from typing import Any

from pyport import PortClient

from src.config import config
from src.models.scorecards import Scorecard
from src.utils import logger
from src.utils.errors import PortError


class PortScorecardClient:
    """Client for interacting with Port Scorecard APIs."""

    def __init__(self, client: PortClient):
        self._client = client

    async def get_scorecards(self, blueprint_identifier: str) -> list[Scorecard]:
        logger.info(f"Getting all scorecards for blueprint '{blueprint_identifier}' from Port")

        response = self._client.scorecards.get_scorecards(blueprint_identifier)

        scorecards_data = response.get("scorecards", [])
        logger.info(f"Got {len(scorecards_data)} scorecards for blueprint '{blueprint_identifier}' from Port")
        logger.debug(f"Response for get scorecards: {response}")

        if config.api_validation_enabled:
            logger.debug("Validating scorecards")
            return [Scorecard(**scorecard_data) for scorecard_data in scorecards_data]
        else:
            logger.debug("Skipping API validation for scorecards")
            return [Scorecard.construct(**scorecard_data) for scorecard_data in scorecards_data]

    async def get_scorecard(self, blueprint_id: str, scorecard_id: str) -> Scorecard:
        logger.info(f"Getting scorecard '{scorecard_id}' from blueprint '{blueprint_id}' from Port")

        scorecards = await self.get_scorecards(blueprint_id)

        logger.info(f"Got {len(scorecards)} scorecards for blueprint '{blueprint_id}' from Port")

        for scorecard in scorecards:
            if scorecard.identifier == scorecard_id:
                logger.info(f"Found scorecard '{scorecard_id}' in blueprint '{blueprint_id}'")
                logger.debug(f"Response for get scorecard: {scorecard.model_dump()}")
                return scorecard

        logger.error(f"Could not find scorecard '{scorecard_id}' in blueprint '{blueprint_id}'")
        raise PortError(f"Could not find scorecard '{scorecard_id}' in blueprint '{blueprint_id}'")

    async def create_scorecard(self, blueprint_id: str, scorecard_data: dict[str, Any]) -> Scorecard:
        logger.info(f"Creating scorecard in blueprint '{blueprint_id}'")
        json_data = json.dumps(scorecard_data)
        logger.debug(f"Input for create scorecard: {json_data}")

        response = self._client.make_request("POST", f"blueprints/{blueprint_id}/scorecards", json=scorecard_data)

        created_data = response.json()
        if not created_data.get("ok"):
            message = f"Failed to create scorecard: {created_data}"
            logger.warning(message)
            raise PortError(message)

        logger.info(f"Created scorecard for blueprint '{blueprint_id}'")

        data = created_data.get("scorecard", {})

        logger.debug(f"Response for create scorecard: {data}")

        if config.api_validation_enabled:
            logger.debug("Validating scorecard")
            return Scorecard(**data)
        else:
            logger.debug("Skipping API validation for scorecard")
            return Scorecard.construct(**data)

    async def delete_scorecard(self, scorecard_id: str, blueprint_id: str) -> bool:
        logger.info(f"Deleting scorecard '{scorecard_id}' from blueprint '{blueprint_id}'")

        response = self._client.make_request("DELETE", f"blueprints/{blueprint_id}/scorecards/{scorecard_id}")
        deleted_data = response.json()
        if not deleted_data.get("ok"):
            message = f"Failed to delete scorecard: {deleted_data}"
            logger.warning(message)
            raise PortError(message)

        logger.info(f"Deleted scorecard '{scorecard_id}' from blueprint '{blueprint_id}'")
        logger.debug(f"Response for delete scorecard: {deleted_data}")
        return True

    async def update_scorecard(self, blueprint_id: str, scorecard_id: str, scorecard_data: dict[str, Any]) -> Scorecard:
        logger.info(f"Updating scorecard '{scorecard_id}' in blueprint '{blueprint_id}'")
        rules = scorecard_data.get("rules", [])
        levels = scorecard_data.get("levels", [])
        # Validate that rules don't reference the first level (base level)
        if rules and len(levels) > 0:
            base_level = levels[0]
            for rule in rules:
                if rule.get("level") == base_level.get("title"):
                    message = f"❌ Error updating scorecard: The base level '{base_level}' cannot have rules associated with it."
                    logger.error(message)
                    raise PortError(message)

        response = self._client.make_request(
            "PUT",
            f"blueprints/{blueprint_id}/scorecards/{scorecard_id}",
            json=scorecard_data,
        )

        updated_data = response.json()
        if not updated_data.get("ok"):
            message = f"Failed to update scorecard: {updated_data}"
            logger.warning(message)
            raise PortError(message)

        logger.info(f"Updated scorecard '{scorecard_id}' in blueprint '{blueprint_id}'")

        data = updated_data.get("scorecard", {})

        logger.debug(f"Response for update scorecard: {data}")

        if config.api_validation_enabled:
            logger.debug("Validating scorecard")
            return Scorecard(**data)
        else:
            logger.debug("Skipping API validation for scorecard")
            return Scorecard.construct(**data)
