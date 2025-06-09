from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.scorecards import Scorecard
from src.models.tools.tool import Tool


class GetScorecardToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get scorecard for")
    scorecard_identifier: str = Field(..., description="The identifier of the scorecard to get")
    detailed: bool = Field(
        default=True,
        description="If True (default), returns complete scorecard details including rules and calculation method. If False, returns summary information only.",
    )


class GetScorecardTool(Tool[GetScorecardToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_scorecard",
            description="Get a specific scorecard for a given blueprint using it's identifier",
            input_schema=GetScorecardToolSchema,
            output_schema=Scorecard,
            annotations=Annotations(
                title="Get Scorecard",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.get_scorecard,
        )
        self.port_client = port_client

    async def get_scorecard(self, props: GetScorecardToolSchema) -> dict[str, Any]:
        args = props.model_dump()

        scorecard_identifier = args.get("scorecard_identifier")
        blueprint_identifier = args.get("blueprint_identifier")

        if not scorecard_identifier or not blueprint_identifier:
            raise ValueError("Scorecard identifier and blueprint identifier are required")

        scorecard = await self.port_client.get_scorecard(blueprint_identifier, scorecard_identifier)
        scorecard_dict = scorecard.model_dump(exclude_unset=True, exclude_none=True)

        return scorecard_dict
