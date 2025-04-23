from loguru import logger
from src.server.client.client import PortClient
from src.server.models import Entity, Annotations
from src.server.models.tools.tool import Tool
from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field
from typing import Any, Dict, List
import types

class GetEntityToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get entity for")
    entity_identifier: str = Field(..., description="The identifier of the entity to get")
    detailed: bool = Field(default=True, description="If True (default), returns complete entity details including properties. If False, returns summary information only.")

class GetEntityTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_entity",
            description="Get an entity from a given blueprint using it's identifier",
            input_schema=GetEntityToolSchema,
            output_schema=Entity,
            annotations=Annotations(
                title="Get Entity",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False
            ),
            function=self.get_entity,
        )
        self.port_client = port_client

    async def get_entity(self, props: GetEntityToolSchema) -> List[Dict[str, Any]]:
        args = props.model_dump()
        blueprint_identifier = args.get("blueprint_identifier")
        entity_identifier = args.get("entity_identifier")
        detailed = args.get("detailed")
        logger.info(f"Retrieving entity '{entity_identifier}' from blueprint '{blueprint_identifier}' (detailed={detailed})")
        result = await self.port_client.get_entity(blueprint_identifier, entity_identifier)
        result_dict = result.model_dump(exclude_unset=True, exclude_none=True)
        return result_dict