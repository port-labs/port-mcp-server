import json
from typing import Any, Dict
from loguru import logger
from src.server.utils import PortError
from src.server.models.entities import Entity, CreateEntity
from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field
from src.server.models.tools.tool import Tool
from src.server.client.client import PortClient
import mcp.types as types
from pydantic.json_schema import SkipJsonSchema

    
class UpdateEntityToolSchema(BaseModel):
    entity_identifier: str | SkipJsonSchema[None] = Field(default=None, description="The identifier of the entity to update")
    entity: CreateEntity = Field(..., description="The entity to update")
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to update the entity for")

class UpdateEntityTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_entity",
            description="Update an entity for a specific blueprint using it's identifier",
            input_schema=UpdateEntityToolSchema,
            output_schema=Entity,
            function=self.update_entity,
        )
        self.port_client = port_client

    async def update_entity(self, props: UpdateEntityToolSchema) -> Dict[str, Any]:
        blueprint_identifier = props.blueprint_identifier
        entity_identifier = props.entity_identifier
        logger.info(f"Updating entity for blueprint '{blueprint_identifier}' in Port")
        
        data = props.entity.dict(exclude_unset=True, exclude_none=True)
        result = await self.port_client.update_entity(blueprint_identifier, entity_identifier, data)
        return result.dict(exclude_unset=True, exclude_none=True)
