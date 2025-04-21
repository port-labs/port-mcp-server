from typing import Any, Dict
from src.mcp_server_port.models import Blueprint
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field
from loguru import logger
from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.tools.tool import Tool
import mcp.types as types

class GetBlueprintsToolSchema(BaseModel):
    detailed: bool = Field(default=True, description="Whether to return detailed blueprints")


class GetBlueprintsToolResponse(BaseModel):
    blueprints: list[Blueprint] = Field(description="The list of blueprints")

class GetBlueprintsTool(Tool):
    """Get blueprints from Port"""
    port_client: PortClient
    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_blueprints",
            description="Get all of the blueprints in your organization",
            input_schema=GetBlueprintsToolSchema,
            output_schema=GetBlueprintsToolResponse,
            function=self.get_blueprints,
        )
        self.port_client = port_client
    
    async def get_blueprints(self, props: GetBlueprintsToolSchema) -> Dict[str, Any]:
        logger.info(f"Getting blueprints with props: {props}")
        args = props.dict()
        detailed = args.get("detailed")
        
        logger.info(f"Retrieving all blueprints from Port (detailed={detailed})")
        blueprints = await self.port_client.get_blueprints()
        logger.info(f"Blueprints: {blueprints}")
        blueprints = GetBlueprintsToolResponse(blueprints=blueprints)
        return blueprints.dict()