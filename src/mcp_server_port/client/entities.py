import logging
from typing import Dict, Any, Union
import requests
from pyport import PortClient
from src.mcp_server_port.models.entities import Entity
from src.mcp_server_port.utils import PortError

logger = logging.getLogger(__name__)

class PortEntityClient:
    """Client for interacting with Port Entity APIs."""
    _client: PortClient
    def __init__(self, client: PortClient):
        self._client = client

    async def get_entities(self, blueprint_identifier: str) -> Union[list[Entity], str]:
        if not self._client:
            raise PortError("Cannot get entities: Port client not initialized with credentials")
        
        logger.info(f"Getting entities for blueprint '{blueprint_identifier}' from Port")
        
        # Use the SDK's entities methods
        entities_data = self._client.entities.get_entities(blueprint_identifier)
        logger.info(f"Entities data: {entities_data}")
        entity_list = [Entity(**entity_data) for entity_data in entities_data]
        return entity_list
            
    
    async def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> Union[Entity, str]:
        if not self._client:
            raise PortError("Cannot get entity: Port client not initialized with credentials")
        
        logger.info(f"Getting entity '{entity_identifier}' from blueprint '{blueprint_identifier}' from Port")
        # Use the SDK's entities methods
        entity_data = self._client.entities.get_entity(blueprint_identifier, entity_identifier)
        logger.info(f"Entity data: {entity_data}")
        return Entity(**entity_data)
            
    
    async def create_entity(self, blueprint_identifier: str, entity_data: Dict[str, Any],query: Dict[str, Any]) -> Entity:
        if not self._client:
            raise PortError("Cannot create entity: Port client not initialized with credentials")
        
        logger.info(f"Creating entity for blueprint '{blueprint_identifier}' in Port")
        
        # Use the SDK's entities methods
        url = f"blueprints/{blueprint_identifier}/entities"
        query_str = (f"upsert={query.get('upsert',False)}&"
               f"validation_only={query.get('validation_only',False)}&"
               f"create_missing_related_entities={query.get('create_missing_related_entities',False)}&"
               f"merge={query.get('merge',False)}").lower()
        response = self._client.make_request('POST', f"{url}?{query_str}", json=entity_data)
        created_data = response.json()
        if created_data.get("ok"):
            entity = created_data.get("entity",{})
            logger.info(f"Created data: {created_data}")           
            return Entity(**entity)
        else:
            raise PortError(f"Failed to create entity: {created_data}")
            
    
    async def update_entity(self, blueprint_identifier: str, entity_identifier: str, entity_data: Dict[str, Any]) -> Entity:
        if not self._client:
            raise PortError("Cannot update entity: Port client not initialized with credentials")
        
        logger.info(f"Updating entity '{entity_identifier}' in blueprint '{blueprint_identifier}' in Port")
        
        # Use the SDK's entities methods
        updated_data = self._client.entities.update_entity(blueprint_identifier, entity_identifier, entity_data)
        if updated_data.get("ok"):
            entity = updated_data.get("entity",{})
            logger.info(f"Updated data: {updated_data}")           
            return Entity(**entity)
        else:
            raise PortError(f"Failed to update entity: {updated_data}")
            
    async def delete_entity(self, blueprint_identifier: str, entity_identifier: str) -> bool:
        if not self._client:
            raise PortError("Cannot delete entity: Port client not initialized with credentials")
        
        logger.info(f"Deleting entity '{entity_identifier}' from blueprint '{blueprint_identifier}' in Port")
        return self._client.entities.delete_entity(blueprint_identifier, entity_identifier)
