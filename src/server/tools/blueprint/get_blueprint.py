from src.server.models import Blueprint, Annotations
from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field
from loguru import logger
from src.server.models.tools.tool import Tool
from src.server.client.client import PortClient
from typing import Any, Dict

class GetBlueprintToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get")
    detailed: bool = Field(default=True, description="Whether to get the detailed blueprint")

class GetBlueprintTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_blueprint",
            description="Get a blueprint using its identifier",
            input_schema=GetBlueprintToolSchema,
            output_schema=Blueprint,
            annotations=Annotations(
                title="Get Blueprint",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False
            ),
            function=self.get_blueprint,
        )
        self.port_client = port_client

    async def get_blueprint(self, props: GetBlueprintToolSchema) -> Dict[str, Any]:
        args = props.model_dump()
        blueprint_id = args.get("blueprint_identifier")
        detailed = args.get("detailed")
        
        blueprint = await self.port_client.get_blueprint(blueprint_id)
        blueprint_dict = blueprint.model_dump(exclude_unset=True, exclude_none=True)
        
        return blueprint_dict