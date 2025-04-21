from typing import Any, Callable, Dict, Optional, Union

from src.mcp_server_port.utils import PortError
import requests

from loguru import logger
import pyport

from src.mcp_server_port.models.scorecards import ScorecardCreate
from src.mcp_server_port.models import PortAgentResponse, Blueprint, Scorecard, Entity, CreateBlueprint
from src.mcp_server_port.config import PORT_API_BASE

from .agent import PortAgentClient
from .blueprints import PortBlueprintClient
from .entities import PortEntityClient
from .scorecards import PortScorecardClient

class PortClient:
    """Client for interacting with the Port API."""
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, region: str = "EU", base_url: str = PORT_API_BASE):
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
    async def wrap_request(self, request:Callable) -> PortError:
        try:
            return await request()
        except requests.exceptions.HTTPError as e:
            self.handle_http_error(e)

    async def trigger_agent(self, prompt: str) -> Dict[str, Any]:
        return await self.wrap_request(lambda: self.agent.trigger_agent(prompt))
    async def get_invocation_status(self, identifier: str) -> PortAgentResponse:
        return await self.wrap_request(lambda: self.agent.get_invocation_status(identifier))
    async def get_blueprints(self) -> Union[list[Blueprint], str]:
        return await self.wrap_request(lambda: self.blueprints.get_blueprints())
    async def get_blueprint(self, blueprint_identifier: str) -> Union[Blueprint, str]:
        return await self.wrap_request(lambda: self.blueprints.get_blueprint(blueprint_identifier))
    async def get_entities(self, blueprint_identifier: str) -> list[Entity]:
        return await self.wrap_request(lambda: self.entities.get_entities(blueprint_identifier))
    async def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> Entity:
        return await self.wrap_request(lambda: self.entities.get_entity(blueprint_identifier, entity_identifier))
    async def create_blueprint(self, blueprint_data: Dict[str, Any]) -> Blueprint:
        return await self.wrap_request(lambda: self.blueprints.create_blueprint(blueprint_data))
    async def update_blueprint(self, blueprint_data: Dict[str, Any]) -> Blueprint:
        return await self.wrap_request(lambda: self.blueprints.update_blueprint(blueprint_data))
    async def create_entity(self, blueprint_identifier: str, entity_data: Dict[str, Any],query: Dict[str, Any]) -> Entity:
        return await self.wrap_request(lambda: self.entities.create_entity(blueprint_identifier, entity_data,query))
    async def update_entity(self, blueprint_identifier: str, entity_identifier: str, entity_data: Dict[str, Any]) -> Entity:
        return await self.wrap_request(lambda: self.entities.update_entity(blueprint_identifier, entity_identifier, entity_data))
    async def get_all_scorecards(self,blueprint_identifier: str) -> Union[list[Scorecard], str]:
        return await self.wrap_request(lambda: self.scorecards.get_scorecards(blueprint_identifier))
    async def get_scorecard_details(self, scorecard_id: str, blueprint_id: str = None) -> Union[Scorecard, str]:
        return await self.wrap_request(lambda: self.scorecards.get_scorecard(scorecard_id, blueprint_id))
    async def create_new_scorecard(self, blueprint_id: str, scorecard_data: Dict[str, Any]) -> Scorecard:
        return await self.wrap_request(lambda: self.scorecards.create_scorecard(blueprint_id, scorecard_data))
    async def delete_scorecard(self, scorecard_id: str, blueprint_id: str) -> bool:
        return await self.wrap_request(lambda: self.scorecards.delete_scorecard(scorecard_id, blueprint_id)) 
    async def update_scorecard(self, blueprint_id: str, scorecard_data: Dict[str, Any]) -> Scorecard:
        return await self.wrap_request(lambda: self.scorecards.update_scorecard(blueprint_id, scorecard_data))
    async def delete_entity(self, blueprint_identifier: str, entity_identifier: str) -> bool:
        return await self.wrap_request(lambda: self.entities.delete_entity(blueprint_identifier, entity_identifier))
    async def delete_blueprint(self, blueprint_identifier: str) -> bool:
        return await self.wrap_request(lambda: self.blueprints.delete_blueprint(blueprint_identifier))