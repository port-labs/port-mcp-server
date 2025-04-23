from typing import Any, Dict, List
from src.server.models import Blueprint
from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field
from loguru import logger
from src.server.client.client import PortClient
from src.server.models import Annotations
from src.server.models.tools.tool import Tool

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
            annotations=Annotations(
                title="Get Blueprints",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False
            ),
            function=self.get_blueprints,
        )
        self.port_client = port_client
    
    async def get_blueprints(self, props: GetBlueprintsToolSchema) -> Dict[str, Any]:
        args = props.model_dump()
        detailed = args.get("detailed")
        
        blueprints = await self.port_client.get_blueprints()
        blueprints = GetBlueprintsToolResponse(blueprints=blueprints)
        return blueprints.model_dump()