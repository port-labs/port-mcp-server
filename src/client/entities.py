from typing import Any, cast

from pyport import PortClient

from src.config import config
from src.models.entities import EntityResult
from src.utils import PortError, logger


class PortEntityClient:
    """Client for interacting with Port Entity APIs."""

    _client: PortClient

    def __init__(self, client: PortClient):
        self._client = client

    async def get_entities(self, blueprint_identifier: str) -> list[EntityResult]:
        logger.info(f"Getting entities for blueprint '{blueprint_identifier}' from Port")

        entities_data = self._client.entities.get_entities(blueprint_identifier)

        logger.info(f"Got {len(entities_data)} entities for blueprint '{blueprint_identifier}' from Port")
        logger.debug(f"Response for get entities: {entities_data}")
        if config.api_validation_enabled:
            logger.debug("Validating entities")
            return [EntityResult(**entity_data) for entity_data in entities_data]
        else:
            logger.debug("Skipping API validation for entities")
            return [EntityResult.construct(**entity_data) for entity_data in entities_data]

    async def search_entities(
        self, 
        blueprint_identifier: str, 
        query: dict[str, Any] | None = None,
        include: list[str] | None = None,
        limit: int = 200
    ) -> list[EntityResult]:
        logger.info(f"Searching entities for blueprint '{blueprint_identifier}' from Port")
        
        # Build request body according to API spec
        request_body: dict[str, Any] = {}
        
        if query:
            request_body["query"] = query
            
        if include:
            request_body["include"] = include
            
        if limit:
            request_body["limit"] = limit
            
        logger.debug(f"Search request body: {request_body}")

        endpoint = f"blueprints/{blueprint_identifier}/entities/search"

        response = self._client.make_request(method="POST", endpoint=endpoint, json=request_body)
        response_data = response.json()

        if not response_data.get("ok"):
            message = f"Failed to search entities: {response_data}"
            logger.warning(message)
            raise PortError(message)
        
        entities_data = response_data.get("entities", [])

        logger.info(f"Got {len(entities_data)} entities for blueprint '{blueprint_identifier}' from Port")
        if config.api_validation_enabled:
            logger.debug("Validating entities")
            return [EntityResult(**entity_data) for entity_data in entities_data]
        else:
            logger.debug("Skipping API validation for entities")
            return [EntityResult.construct(**entity_data) for entity_data in entities_data]

    async def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> EntityResult:
        logger.info(f"Getting entity '{entity_identifier}' from blueprint '{blueprint_identifier}' from Port")

        entity_data = self._client.entities.get_entity(blueprint_identifier, entity_identifier)

        logger.info(f"Got entity '{entity_identifier}' from blueprint '{blueprint_identifier}' from Port")
        logger.debug(f"Response for get entity: {entity_data}")
        if config.api_validation_enabled:
            logger.debug("Validating entity")
            return EntityResult(**entity_data)
        else:
            logger.debug("Skipping API validation for entity")
            return EntityResult.construct(**entity_data)

    async def create_entity(self, blueprint_identifier: str, entity_data: dict[str, Any], query: dict[str, Any]) -> EntityResult:
        logger.info(f"Creating entity for blueprint '{blueprint_identifier}' in Port")
        logger.debug(f"Input from tool to create entity: {entity_data}")

        url = f"blueprints/{blueprint_identifier}/entities"
        query_str = (
            f"upsert={query.get('upsert', False)}&"
            f"validation_only={query.get('validation_only', False)}&"
            f"create_missing_related_entities={query.get('create_missing_related_entities', False)}&"
            f"merge={query.get('merge', False)}"
        ).lower()

        response = self._client.make_request("POST", f"{url}?{query_str}", json=entity_data)
        created_data = response.json()

        if not created_data.get("ok"):
            message = f"Failed to create entity: {created_data}"
            logger.warning(message)
            raise PortError(message)

        logger.info(f"Created entity for blueprint '{blueprint_identifier}' in Port")

        entity = created_data.get("entity", {})

        logger.debug(f"Response for create entity: {entity}")
        if config.api_validation_enabled:
            logger.debug("Validating entity")
            return EntityResult(**entity)
        else:
            logger.debug("Skipping API validation for entity")
            return EntityResult.construct(**entity)

    async def update_entity(self, blueprint_identifier: str, entity_identifier: str, entity_data: dict[str, Any]) -> EntityResult:
        logger.info(f"Updating entity '{entity_identifier}' in blueprint '{blueprint_identifier}' in Port")
        logger.debug(f"Input from tool to update entity: {entity_data}")

        updated_data = self._client.entities.update_entity(blueprint_identifier, entity_identifier, entity_data)
        if not updated_data.get("ok"):
            message = f"Failed to update entity: {updated_data}"
            logger.warning(message)
            raise PortError(message)

        logger.info(f"Updated entity '{entity_identifier}' in blueprint '{blueprint_identifier}' in Port")

        entity = updated_data.get("entity", {})
        logger.debug(f"Response for update entity: {entity}")

        if config.api_validation_enabled:
            logger.debug("Validating entity")
            return EntityResult(**entity)
        else:
            logger.debug("Skipping API validation for entity")
            return EntityResult.construct(**entity)

    async def delete_entity(self, blueprint_identifier: str, entity_identifier: str, delete_dependents: bool = False) -> bool:
        logger.info(f"Deleting entity '{entity_identifier}' from blueprint '{blueprint_identifier}' in Port")
        logger.debug(f"Input from tool to delete entity: {delete_dependents}")

        url = f"blueprints/{blueprint_identifier}/entities/{entity_identifier}"
        query_str = f"delete_dependents={delete_dependents}".lower()
        response = self._client.make_request("DELETE", f"{url}?{query_str}")
        response_json = response.json()
        if not response_json.get("ok"):
            message = f"Failed to delete entity: {response_json}"
            logger.warning(message)
            raise PortError(message)
        logger.info(f"Deleted entity '{entity_identifier}' from blueprint '{blueprint_identifier}' in Port")
        return cast(bool, response_json.get("ok"))
