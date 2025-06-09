from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.scorecards import Scorecard, ScorecardUpdate
from src.models.tools.tool import Tool


class UpdateScorecardToolSchema(ScorecardUpdate):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to create the scorecard for")
    scorecard_identifier: str = Field(..., description="The identifier of the scorecard to update")


class UpdateScorecardTool(Tool[UpdateScorecardToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_scorecard",
            description="Update a scorecard for a specific blueprint using its identifier",
            function=self.update_scorecard,
            input_schema=UpdateScorecardToolSchema,
            output_schema=Scorecard,
            annotations=Annotations(
                title="Update Scorecard",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True,
            ),
        )
        self.port_client = port_client

    async def update_scorecard(self, props: UpdateScorecardToolSchema) -> dict[str, Any]:
        args = props.model_dump()
        blueprint_identifier = args.get("blueprint_identifier")
        scorecard_identifier = args.get("scorecard_identifier")
        scorecard_data = props.model_dump(exclude_none=True, exclude_unset=True)
        scorecard_data.pop("blueprint_identifier")
        scorecard_data.pop("scorecard_identifier")

        if not blueprint_identifier or not scorecard_identifier:
            raise ValueError("Blueprint identifier and scorecard identifier are required")

        created_scorecard = await self.port_client.update_scorecard(blueprint_identifier, scorecard_identifier, scorecard_data)
        created_scorecard_dict = created_scorecard.model_dump(exclude_unset=True, exclude_none=True)

        return created_scorecard_dict
