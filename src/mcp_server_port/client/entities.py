import logging
from typing import Dict, Any, Union
from ..models.models import PortEntity, PortEntityList
from ..utils import PortError

logger = logging.getLogger(__name__)

class PortEntityClient:
    """Client for interacting with Port Entity APIs."""
    
    def __init__(self, client):
        self._client = client

    async def get_entities(self, blueprint_identifier: str) -> Union[PortEntityList, str]:
        """
        Get all entities for a specific blueprint.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            
        Returns:
            PortEntityList: A list of entities
            str: Formatted text representation of entities if to_text=True
        """
        if not self._client:
            raise PortError("Cannot get entities: Port client not initialized with credentials")
        
        try:
            logger.info(f"Getting entities for blueprint '{blueprint_identifier}' from Port")
            
            # Use the SDK's entities methods
            entities_data = self._client.entities.get_entities(blueprint_identifier)
            entities = []
            
            for entity_data in entities_data:
                entity = PortEntity(
                    identifier=entity_data.get("identifier", ""),
                    title=entity_data.get("title", "Untitled Entity"),
                    blueprint=blueprint_identifier,
                    icon=entity_data.get("icon"),
                    properties=entity_data.get("properties", {}),
                    relations=entity_data.get("relations", {}),
                    team=entity_data.get("team"),
                    created_at=entity_data.get("createdAt"),
                    created_by=entity_data.get("createdBy"),
                    updated_at=entity_data.get("updatedAt"),
                    updated_by=entity_data.get("updatedBy")
                )
                entities.append(entity)
            
            entity_list = PortEntityList(
                entities=entities,
                blueprint_identifier=blueprint_identifier
            )
            return entity_list
            
        except Exception as e:
            logger.error(f"Error in get_entities: {str(e)}")
            raise PortError(f"Error getting entities for blueprint '{blueprint_identifier}': {str(e)}")
    
    async def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> Union[PortEntity, str]:
        """
        Get a specific entity by identifier.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            entity_identifier: The identifier of the entity
            
        Returns:
            PortEntity: The entity object
            str: Formatted text representation of the entity if to_text=True
        """
        if not self._client:
            raise PortError("Cannot get entity: Port client not initialized with credentials")
        
        try:
            logger.info(f"Getting entity '{entity_identifier}' from blueprint '{blueprint_identifier}' from Port")
            
            # Use the SDK's entities methods
            entity_data = self._client.entities.get_entity(blueprint_identifier, entity_identifier)
            
            entity = PortEntity(
                identifier=entity_data.get("identifier", ""),
                title=entity_data.get("title", "Untitled Entity"),
                blueprint=blueprint_identifier,
                icon=entity_data.get("icon"),
                properties=entity_data.get("properties", {}),
                relations=entity_data.get("relations", {}),
                team=entity_data.get("team"),
                created_at=entity_data.get("createdAt"),
                created_by=entity_data.get("createdBy"),
                updated_at=entity_data.get("updatedAt"),
                updated_by=entity_data.get("updatedBy")
            )
            
            return entity
            
        except Exception as e:
            logger.error(f"Error in get_entity: {str(e)}")
            raise PortError(f"Error getting entity '{entity_identifier}' from blueprint '{blueprint_identifier}': {str(e)}")
    
    async def create_entity(self, blueprint_identifier: str, entity_data: Dict[str, Any]) -> PortEntity:
        """
        Create a new entity for a blueprint.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            entity_data: Data for the entity to create
            
        Returns:
            PortEntity: The created entity
        """
        if not self._client:
            raise PortError("Cannot create entity: Port client not initialized with credentials")
        
        try:
            logger.info(f"Creating entity for blueprint '{blueprint_identifier}' in Port")
            
            # Use the SDK's entities methods
            created_data = self._client.entities.create_entity(blueprint_identifier, entity_data)
            
            created_entity = PortEntity(
                identifier=created_data.get("identifier", ""),
                title=created_data.get("title", "Untitled Entity"),
                blueprint=blueprint_identifier,
                icon=created_data.get("icon"),
                properties=created_data.get("properties", {}),
                relations=created_data.get("relations", {}),
                team=created_data.get("team"),
                created_at=created_data.get("createdAt"),
                created_by=created_data.get("createdBy"),
                updated_at=created_data.get("updatedAt"),
                updated_by=created_data.get("updatedBy")
            )
            
            return created_entity
            
        except Exception as e:
            logger.error(f"Error in create_entity: {str(e)}")
            raise PortError(f"Error creating entity for blueprint '{blueprint_identifier}': {str(e)}")
    
    async def update_entity(self, blueprint_identifier: str, entity_identifier: str, entity_data: Dict[str, Any]) -> PortEntity:
        """
        Update an existing entity.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            entity_identifier: The identifier of the entity to update
            entity_data: Updated data for the entity
            
        Returns:
            PortEntity: The updated entity
        """
        if not self._client:
            raise PortError("Cannot update entity: Port client not initialized with credentials")
        
        try:
            logger.info(f"Updating entity '{entity_identifier}' in blueprint '{blueprint_identifier}' in Port")
            
            # Use the SDK's entities methods
            updated_data = self._client.entities.update_entity(blueprint_identifier, entity_identifier, entity_data)
            
            updated_entity = PortEntity(
                identifier=updated_data.get("identifier", ""),
                title=updated_data.get("title", "Untitled Entity"),
                blueprint=blueprint_identifier,
                icon=updated_data.get("icon"),
                properties=updated_data.get("properties", {}),
                relations=updated_data.get("relations", {}),
                team=updated_data.get("team"),
                created_at=updated_data.get("createdAt"),
                created_by=updated_data.get("createdBy"),
                updated_at=updated_data.get("updatedAt"),
                updated_by=updated_data.get("updatedBy")
            )
            
            return updated_entity
            
        except Exception as e:
            logger.error(f"Error in update_entity: {str(e)}")
            raise PortError(f"Error updating entity '{entity_identifier}' in blueprint '{blueprint_identifier}': {str(e)}") 