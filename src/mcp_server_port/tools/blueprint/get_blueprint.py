from src.mcp_server_port.models import Blueprint
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field
from loguru import logger
from src.mcp_server_port.models.tools.tool import Tool
from src.mcp_server_port.client.client import PortClient
from typing import Any, Dict

class GetBlueprintToolSchema(BaseModel):
    blueprint_id: str = Field(..., description="The identifier of the blueprint to get")
    detailed: bool = Field(default=True, description="Whether to get the detailed blueprint")

class GetBlueprintTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_blueprint",
            description="Get a blueprint using it's identifier",
            input_schema=GetBlueprintToolSchema,
            output_schema=Blueprint,
            function=self.get_blueprint,
        )
        self.port_client = port_client

    async def get_blueprint(self, props: GetBlueprintToolSchema) -> Dict[str, Any]:
        args = props.dict()
        blueprint_id = args.get("blueprint_id")
        detailed = args.get("detailed")
        
        logger.info(f"Retrieving blueprint with identifier: {blueprint_id} (detailed={detailed})")
        blueprint = await self.port_client.get_blueprint(blueprint_id)
        blueprint_dict = blueprint.dict(exclude_unset=True, exclude_none=True)
        logger.info(f"Blueprint: {blueprint_dict}")
        return blueprint_dict