import logging
import json
from typing import Any, Dict, Union

from pyport import PortClient
import requests
from src.mcp_server_port.models import Blueprint,CreateBlueprint
from src.mcp_server_port.utils import PortError

logger = logging.getLogger(__name__)

class PortBlueprintClient:
    """Client for interacting with Port Blueprint APIs."""
    
    def __init__(self, client:PortClient):
        self._client = client

    async def get_blueprints(self) -> list[Blueprint]:
        if not self._client:
            raise PortError("Cannot get blueprints: Port client not initialized with credentials")
        
        logger.info("Getting blueprints from Port")

        blueprints = self._client.blueprints.get_blueprints()

        logger.info(f"Blueprints: {blueprints}")

        return [Blueprint(**bp) for bp in blueprints]

    async def get_blueprint(self, blueprint_identifier: str) -> Union[Blueprint, str]:
        if not self._client:
            raise PortError("Cannot get blueprint: Port client not initialized with credentials")
        
        logger.info(f"Getting blueprint '{blueprint_identifier}' from Port")
        
        bp_data = self._client.blueprints.get_blueprint(blueprint_identifier)
        
        logger.info(f"Blueprint data: {bp_data}")
        
        return Blueprint(**bp_data)
            
    async def create_blueprint(self, blueprint_data: Dict[str, Any]) -> Blueprint:
        data_json = json.dumps(blueprint_data)
        logger.info(f"Creating blueprint: {data_json}")
        response = self._client.make_request("POST", f"blueprints", json=blueprint_data)
        result = response.json()
        if not result.get("ok"):
            raise PortError(f"Error creating blueprint: {result.get('error')}")
        
        result = result.get("blueprint", {})
        blueprint = Blueprint(**result)
        logger.info(f"Blueprint created: {blueprint}")
        return blueprint

    async def update_blueprint(self, blueprint_data: Dict[str, Any]) -> Blueprint:
        data_json = json.dumps(blueprint_data)
        logger.info(f"Updating blueprint: {data_json}")
        response = self._client.make_request("PATCH", f"blueprints/{blueprint_data.get('identifier')}", json=blueprint_data)
        result = response.json()
        if not result.get("ok"):
            raise PortError(f"Error creating blueprint: {result.get('error')}")
        
        result = result.get("blueprint", {})
        blueprint = Blueprint(**result)
        logger.info(f"Blueprint created: {blueprint}")
        return blueprint
    
    async def delete_blueprint(self, blueprint_identifier: str) -> bool:
        return self._client.blueprints.delete_blueprint(blueprint_identifier)