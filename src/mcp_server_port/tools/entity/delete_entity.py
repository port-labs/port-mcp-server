import json
from typing import Any, Dict
from loguru import logger
from src.mcp_server_port.utils import PortError
from src.mcp_server_port.models.entities import Entity, CreateEntity
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field
from src.mcp_server_port.models.tools.tool import Tool
from src.mcp_server_port.client.client import PortClient
import mcp.types as types
from pydantic.json_schema import SkipJsonSchema

    
class DeleteEntityToolSchema(BaseModel):
    entity_identifier: str = Field(..., description="The identifier of the entity to delete")
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to delete the entity for")
    delete_dependents: bool = Field(default=False, description="If true, this call will also delete all of the entity's dependents")
    run_id: str = Field(default=None, description="The run_id of the action to delete the entity for")

class DeleteEntityTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="delete_entity",
            description="Delete an entity for a specific blueprint using it's identifier",
            input_schema=DeleteEntityToolSchema,
            output_schema=Entity,
            function=self.delete_entity,
        )
        self.port_client = port_client

    async def delete_entity(self, props: DeleteEntityToolSchema) -> Dict[str, Any]:
        blueprint_identifier = props.blueprint_identifier
        entity_identifier = props.entity_identifier
        logger.info(f"Deleting entity for blueprint '{blueprint_identifier}' in Port")
        
        result = await self.port_client.delete_entity(blueprint_identifier, entity_identifier)
        return {"success": result}
