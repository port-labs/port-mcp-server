
from loguru import logger
from src.mcp_server_port.models.entities import Entity
from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.tools.tool import Tool
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field
import mcp.types as types
from src.mcp_server_port.utils import PortError
class GetEntityToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint the entity belongs to")
    entity_identifier: str = Field(..., description="The unique identifier of the entity to retrieve")
    detailed: bool = Field(default=True, description="If True (default), returns complete entity details. If False, returns summary information only.")

class GetEntityTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_entity",
            description="Get an entity from a given blueprint using it's identifier",
            input_schema=GetEntityToolSchema,
            output_schema=Entity,
            function=self.get_entity,
        )
        self.port_client = port_client
    async def get_entity(self, props: GetEntityToolSchema) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        args = props.dict()
        blueprint_identifier = args.get("blueprint_identifier")
        entity_identifier = args.get("entity_identifier")
        detailed = args.get("detailed")
        logger.info(f"Retrieving entity '{entity_identifier}' from blueprint '{blueprint_identifier}' (detailed={detailed})")
        result = await self.port_client.get_entity(blueprint_identifier, entity_identifier)
        return result.dict(exclude_unset=True, exclude_none=True)