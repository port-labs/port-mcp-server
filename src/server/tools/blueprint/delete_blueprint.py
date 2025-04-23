from typing import Any, Dict
from loguru import logger
from src.server.models import Blueprint, Annotations
from src.server.models.tools.tool import Tool
from src.server.client.client import PortClient
from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field

class DeleteBlueprintToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to delete")


class DeleteBlueprintTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="delete_blueprint",
            description="Delete a blueprint using its identifier",
            input_schema=DeleteBlueprintToolSchema,
            output_schema=Blueprint,
            annotations=Annotations(
                title="Delete Blueprint",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True
            ),
            function=self.delete_blueprint,
        )
        self.port_client = port_client

    async def delete_blueprint(self, props: DeleteBlueprintToolSchema) -> Dict[str, Any]:
        args = props.model_dump()
        blueprint_identifier = args.get('blueprint_identifier')
        result = await self.port_client.delete_blueprint(blueprint_identifier)
        return {"success": result}