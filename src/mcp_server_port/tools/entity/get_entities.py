from loguru import logger
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field
from src.mcp_server_port.models.tools.tool import Tool
from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.entities import Entity
from typing import Any, Dict
class GetEntitiesToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get entities for")
    detailed: bool = Field(default=False, description="If True (default), returns complete entity details including properties and relations. If False, returns summary information only.")


class GetEntitiesToolResponse(BaseModel):
    entities: list[Entity] = Field(..., description="The list of entities")

class GetEntitiesTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_entities",
            description="Get all of the entities for a given blueprint",
            input_schema=GetEntitiesToolSchema,
            output_schema=GetEntitiesToolResponse,
            function=self.get_entities,
        )
        self.port_client = port_client

    async def get_entities(self, props: GetEntitiesToolSchema) -> Dict[str, Any]:
        args = props.dict()
        blueprint_identifier = args.get("blueprint_identifier")
        detailed = args.get("detailed")
        logger.info(f"Retrieving entities for blueprint '{blueprint_identifier}' from Port (detailed={detailed})")
        result = await self.port_client.get_entities(blueprint_identifier)
        entities = GetEntitiesToolResponse(entities=result)
        return entities.dict()