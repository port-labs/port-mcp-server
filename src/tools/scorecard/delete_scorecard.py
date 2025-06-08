from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool


class DeleteScorecardToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get scorecard for")
    scorecard_identifier: str = Field(..., description="The identifier of the scorecard to get")


class DeleteScorecardToolResponse(BaseModel):
    success: bool = Field(..., description="Whether the scorecard was deleted successfully")
    message: str = Field(..., description="The message from the operation")


class DeleteScorecardTool(Tool[DeleteScorecardToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="delete_scorecard",
            description="Delete a scorecard from a given blueprint using its identifier",
            input_schema=DeleteScorecardToolSchema,
            output_schema=DeleteScorecardToolResponse,
            annotations=Annotations(
                title="Delete Scorecard",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True,
            ),
            function=self.delete_scorecard,
        )
        self.port_client = port_client

    async def delete_scorecard(self, props: DeleteScorecardToolSchema) -> dict[str, Any]:
        args = props.model_dump()
        scorecard_id = args.get("scorecard_identifier")
        blueprint_id = args.get("blueprint_identifier")

        if not scorecard_id or not blueprint_id:
            raise ValueError("Scorecard identifier and blueprint identifier are required")

        result = await self.port_client.delete_scorecard(scorecard_id, blueprint_id)
        return {"success": result}
