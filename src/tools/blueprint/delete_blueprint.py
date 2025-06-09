from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.blueprints import Blueprint
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool


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
                openWorldHint=True,
            ),
            function=self.delete_blueprint,
        )
        self.port_client = port_client

    async def delete_blueprint(self, props: DeleteBlueprintToolSchema) -> dict[str, Any]:
        args = props.model_dump()
        blueprint_identifier = args.get("blueprint_identifier")
        if not blueprint_identifier:
            raise ValueError("Blueprint identifier is required")

        result = await self.port_client.delete_blueprint(blueprint_identifier)
        return {"success": result}
