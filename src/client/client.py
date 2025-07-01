from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

import pyport
import requests  # type: ignore[import-untyped]

from src.client.action_runs import PortActionRunClient
from src.client.actions import PortActionClient
from src.client.agent import PortAgentClient
from src.client.blueprints import PortBlueprintClient
from src.client.entities import PortEntityClient
from src.client.permissions import PortPermissionsClient
from src.client.scorecards import PortScorecardClient
from src.config import config
from src.models.action_run.action_run import ActionRun
from src.models.actions.action import Action
from src.models.agent import PortAgentResponse
from src.models.agent.port_agent_response import PortAgentTriggerResponse
from src.models.blueprints import Blueprint
from src.models.entities import EntityResult
from src.models.scorecards import Scorecard
from src.utils import PortError, logger
from src.utils.user_agent import get_user_agent

T = TypeVar("T")
class PortClient:
    """Client for interacting with the Port API."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        region: str = "EU",
        base_url: str = config.port_api_base,
    ):
        if not client_id or not client_secret:
            logger.warning("PortClient initialized without credentials")

        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        if client_id and client_secret:
            self._client = pyport.PortClient(
                client_id=client_id,
                client_secret=client_secret,
                us_region=(region == "US"),
            )
            
            self._setup_custom_headers()
            
            self.agent = PortAgentClient(self._client)
            self.blueprints = PortBlueprintClient(self._client)
            self.entities = PortEntityClient(self._client)
            self.scorecards = PortScorecardClient(self._client)
            self.actions = PortActionClient(self._client)
            self.action_runs = PortActionRunClient(self._client)
            self.permissions = PortPermissionsClient(self._client)

    def _setup_custom_headers(self):
        """Setup custom headers for all HTTP requests."""
        user_agent = get_user_agent()
        logger.debug(f"Setting User-Agent header: {user_agent}")
        
        original_make_request = self._client.make_request
        
        def make_request_with_headers(*args, **kwargs):
            """Wrapper to add custom headers to all requests."""
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            
            kwargs['headers']['User-Agent'] = user_agent
            
            return original_make_request(*args, **kwargs)
        
        self._client.make_request = make_request_with_headers

    def handle_http_error(self, e: requests.exceptions.HTTPError) -> PortError:
        result = e.response.json()
        message = (
            f"Error in {e.request.method} {e.request.url} - {e.response.status_code}: {result}"
        )
        logger.error(message)
        raise PortError(message)

    async def wrap_request(self, request: Callable[[], Awaitable[T]]) -> T:
        if self._client is None:
            raise PortError("PortClient is not properly initialized - missing credentials")
        try:
            return await request()
        except requests.exceptions.HTTPError as e:
            raise self.handle_http_error(e) from e

    async def trigger_agent(self, prompt: str) -> PortAgentTriggerResponse:
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
        return await self.wrap_request(
            lambda: self.blueprints.delete_blueprint(blueprint_identifier)
        )

    async def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> EntityResult:
        return await self.wrap_request(
            lambda: self.entities.get_entity(blueprint_identifier, entity_identifier)
        )

    async def get_entities(self, blueprint_identifier: str) -> list[EntityResult]:
        return await self.wrap_request(lambda: self.entities.get_entities(blueprint_identifier))

    async def search_entities(
        self, 
        blueprint_identifier: str, 
        query: dict[str, Any] | None = None,
        include: list[str] | None = None,
        limit: int = 200
    ) -> list[EntityResult]:
        return await self.wrap_request(lambda: self.entities.search_entities(
            blueprint_identifier=blueprint_identifier,
            query=query,
            include=include,
            limit=limit
        ))

    async def create_entity(
        self, blueprint_identifier: str, entity_data: dict[str, Any], query: dict[str, Any]
    ) -> EntityResult:
        return await self.wrap_request(
            lambda: self.entities.create_entity(blueprint_identifier, entity_data, query)
        )

    async def update_entity(
        self, blueprint_identifier: str, entity_identifier: str, entity_data: dict[str, Any]
    ) -> EntityResult:
        return await self.wrap_request(
            lambda: self.entities.update_entity(
                blueprint_identifier, entity_identifier, entity_data
            )
        )

    async def delete_entity(
        self, blueprint_identifier: str, entity_identifier: str, delete_dependents: bool = False
    ) -> bool:
        return await self.wrap_request(
            lambda: self.entities.delete_entity(
                blueprint_identifier, entity_identifier, delete_dependents
            )
        )

    async def get_scorecard(self, blueprint_id: str, scorecard_id: str) -> Scorecard:
        return await self.wrap_request(
            lambda: self.scorecards.get_scorecard(blueprint_id, scorecard_id)
        )

    async def get_scorecards(self, blueprint_identifier: str) -> list[Scorecard]:
        return await self.wrap_request(lambda: self.scorecards.get_scorecards(blueprint_identifier))

    async def create_scorecard(
        self, blueprint_id: str, scorecard_data: dict[str, Any]
    ) -> Scorecard:
        return await self.wrap_request(
            lambda: self.scorecards.create_scorecard(blueprint_id, scorecard_data)
        )

    async def update_scorecard(
        self, blueprint_id: str, scorecard_id: str, scorecard_data: dict[str, Any]
    ) -> Scorecard:
        return await self.wrap_request(
            lambda: self.scorecards.update_scorecard(blueprint_id, scorecard_id, scorecard_data)
        )

    async def delete_scorecard(self, scorecard_id: str, blueprint_id: str) -> bool:
        return await self.wrap_request(
            lambda: self.scorecards.delete_scorecard(scorecard_id, blueprint_id)
        )

    async def get_all_actions(self, trigger_type: str = "self-service") -> list[Action]:
        return await self.wrap_request(lambda: self.actions.get_all_actions(trigger_type))

    async def get_action(self, action_identifier: str) -> Action:
        return await self.wrap_request(lambda: self.actions.get_action(action_identifier))
    
    async def create_action(self, action_data: dict[str, Any]) -> Action:
        return await self.wrap_request(lambda: self.actions.create_action(action_data))

    async def update_action(self, action_identifier: str, action_data: dict[str, Any]) -> Action:
        return await self.wrap_request(
            lambda: self.actions.update_action(action_identifier, action_data)
        )

    async def delete_action(self, action_identifier: str) -> bool:
        return await self.wrap_request(lambda: self.actions.delete_action(action_identifier))
    
    async def create_global_action_run(self, action_identifier: str, **kwargs) -> ActionRun:
        return await self.wrap_request(
            lambda: self.action_runs.create_global_action_run(action_identifier, **kwargs)
        )

    async def create_entity_action_run(self, action_identifier: str, **kwargs) -> ActionRun:
        return await self.wrap_request(
            lambda: self.action_runs.create_entity_action_run(action_identifier, **kwargs)
        )

    async def get_action_run(self, run_id: str) -> ActionRun:
        return await self.wrap_request(lambda: self.action_runs.get_action_run(run_id))

    async def get_action_permissions(self, action_identifier: str) -> dict[str, Any]:
        return await self.wrap_request(lambda: self.permissions.get_action_permissions(action_identifier))

    async def update_action_policies(self, action_identifier: str, policies: dict[str, Any]) -> dict[str, Any]:
        return await self.wrap_request(lambda: self.permissions.update_action_policies(action_identifier, policies))
