from pydantic import Field
from loguru import logger
from src.server.models import Scorecard, ScorecardCreate, Annotations
from src.server.models.tools.tool import Tool
from src.server.client.client import PortClient
from typing import Any, Dict

class UpdateScorecardToolSchema(ScorecardCreate):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to create the scorecard for")
    scorecard_identifier: str = Field(..., description="The identifier of the scorecard to update")
class UpdateScorecardTool(Tool):
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
                openWorldHint=True
            ),
        )
        self.port_client = port_client

    async def update_scorecard(
        self,
        props: UpdateScorecardToolSchema
    ) -> Dict[str, Any]:
        args = props.model_dump()
        blueprint_identifier = args.get("blueprint_identifier")

        scorecard_data = props.model_dump(exclude_none=True,exclude_unset=True)
        scorecard_data.pop("blueprint_identifier")
        scorecard_data.pop("scorecard_identifier")

        created_scorecard = await self.port_client.update_scorecard(blueprint_identifier, scorecard_data)
        created_scorecard_dict = created_scorecard.model_dump(exclude_unset=True, exclude_none=True)
        
        return created_scorecard_dict