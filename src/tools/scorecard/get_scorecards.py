from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.scorecards import Scorecard
from src.models.tools.tool import Tool


class GetScorecardsToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get scorecards for")
    detailed: bool = Field(
        default=False,
        description="""If True (default), returns complete scorecard details including rules and calculation method. If False, returns summary information only.""",
    )


class GetScorecardsToolResponse(BaseModel):
    scorecards: list[Scorecard] = Field(..., description="The list of scorecards")


class GetScorecardsTool(Tool[GetScorecardsToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_scorecards",
            description="Get all of the scorecards for a given blueprint",
            input_schema=GetScorecardsToolSchema,
            output_schema=GetScorecardsToolResponse,
            annotations=Annotations(
                title="Get Scorecards",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.get_scorecards,
        )
        self.port_client = port_client

    async def get_scorecards(self, props: GetScorecardsToolSchema) -> dict[str, Any]:
        args = props.model_dump()

        blueprint_identifier = args.get("blueprint_identifier")

        if not blueprint_identifier:
            raise ValueError("Blueprint identifier is required")

        raw_scorecards = await self.port_client.get_scorecards(blueprint_identifier)
        processed_scorecards = [scorecard.model_dump(exclude_unset=True, exclude_none=True) for scorecard in raw_scorecards]

        response = GetScorecardsToolResponse.construct(scorecards=processed_scorecards)

        return response.model_dump(exclude_unset=True, exclude_none=True)
