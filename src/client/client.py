from collections.abc import Callable
from typing import Any

import pyport
import requests

from src.client.agent import PortAgentClient
from src.client.blueprints import PortBlueprintClient
from src.client.entities import PortEntityClient
from src.client.scorecards import PortScorecardClient
from src.config import config
from src.models.agent import PortAgentResponse
from src.models.blueprints import Blueprint
from src.models.entities import EntityResult
from src.models.scorecards import Scorecard
from src.utils import PortError, logger


class PortClient:
    """Client for interacting with the Port API."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        region: str = "EU",
        base_url: str = config.port_api_base,
    ):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region

        if not client_id or not client_secret:
            logger.warning("Port client initialized without credentials")
            self._client = None
            self.agent = None
            self.blueprints = None
            self.entities = None
            self.scorecards = None
        else:
            self._client = pyport.PortClient(client_id=client_id, client_secret=client_secret, us_region=(region == "US"))
            self.agent = PortAgentClient(self._client)
            self.blueprints = PortBlueprintClient(self._client)
            self.entities = PortEntityClient(self._client)
            self.scorecards = PortScorecardClient(self._client)

    def handle_http_error(self, e: requests.exceptions.HTTPError) -> PortError:
        result = e.response.json()
        message = f"Error in {e.request.method} {e.request.url} - {e.response.status_code}: {result}"
        logger.error(message)
        raise PortError(message)

    async def wrap_request(self, request: Callable) -> PortError:
        try:
            return await request()
        except requests.exceptions.HTTPError as e:
            self.handle_http_error(e)

    async def trigger_agent(self, prompt: str) -> dict[str, Any]:
        return await self.wrap_request(lambda: self.agent.trigger_agent(prompt))

    async def get_invocation_status(self, identifier: str) -> PortAgentResponse:
        return await self.wrap_request(lambda: self.agent.get_invocation_status(identifier))

    async def get_blueprint(self, blueprint_identifier: str) -> Blueprint:
        return await self.wrap_request(lambda: self.blueprints.get_blueprint(blueprint_identifier))

    async def get_blueprints(self) -> list[Blueprint]:
        return await self.wrap_request(lambda: self.blueprints.get_blueprints())

    async def create_blueprint(self, blueprint_data: dict[str, Any]) -> Blueprint:
        return await self.wrap_request(lambda: self.blueprints.create_blueprint(blueprint_data))

    async def update_blueprint(self, blueprint_data: dict[str, Any]) -> Blueprint:
        return await self.wrap_request(lambda: self.blueprints.update_blueprint(blueprint_data))

    async def delete_blueprint(self, blueprint_identifier: str) -> bool:
        return await self.wrap_request(lambda: self.blueprints.delete_blueprint(blueprint_identifier))

    async def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> EntityResult:
        return await self.wrap_request(lambda: self.entities.get_entity(blueprint_identifier, entity_identifier))

    async def get_entities(self, blueprint_identifier: str) -> list[EntityResult]:
        return await self.wrap_request(lambda: self.entities.get_entities(blueprint_identifier))

    async def create_entity(self, blueprint_identifier: str, entity_data: dict[str, Any], query: dict[str, Any]) -> EntityResult:
        return await self.wrap_request(lambda: self.entities.create_entity(blueprint_identifier, entity_data, query))

    async def update_entity(self, blueprint_identifier: str, entity_identifier: str, entity_data: dict[str, Any]) -> EntityResult:
        return await self.wrap_request(lambda: self.entities.update_entity(blueprint_identifier, entity_identifier, entity_data))

    async def delete_entity(self, blueprint_identifier: str, entity_identifier: str, delete_dependents: bool = False) -> bool:
        return await self.wrap_request(
            lambda: self.entities.delete_entity(blueprint_identifier, entity_identifier, delete_dependents)
        )

    async def get_scorecard(self, blueprint_id: str, scorecard_id: str) -> Scorecard:
        return await self.wrap_request(lambda: self.scorecards.get_scorecard(blueprint_id, scorecard_id))

    async def get_scorecards(self, blueprint_identifier: str) -> list[Scorecard]:
        return await self.wrap_request(lambda: self.scorecards.get_scorecards(blueprint_identifier))

    async def create_scorecard(self, blueprint_id: str, scorecard_data: dict[str, Any]) -> Scorecard:
        return await self.wrap_request(lambda: self.scorecards.create_scorecard(blueprint_id, scorecard_data))

    async def update_scorecard(self, blueprint_id: str, scorecard_id: str, scorecard_data: dict[str, Any]) -> Scorecard:
        return await self.wrap_request(lambda: self.scorecards.update_scorecard(blueprint_id, scorecard_id, scorecard_data))

    async def delete_scorecard(self, scorecard_id: str, blueprint_id: str) -> bool:
        return await self.wrap_request(lambda: self.scorecards.delete_scorecard(scorecard_id, blueprint_id))
