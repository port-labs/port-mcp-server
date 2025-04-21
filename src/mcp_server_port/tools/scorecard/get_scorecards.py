from loguru import logger
from src.mcp_server_port.models.tools import Tool
from src.mcp_server_port.models.scorecards import Scorecard
from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field
from typing import Any, Dict

class GetScorecardsToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get scorecards for")
    detailed: bool = Field(default=False, description="If True (default), returns complete scorecard details including rules and calculation method. If False, returns summary information only.")

class GetScorecardsToolResponse(BaseModel):
    scorecards: list[Scorecard] = Field(..., description="The list of scorecards")

class GetScorecardsTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_scorecards",
            description="Get all of the scorecards for a given blueprint",
            input_schema=GetScorecardsToolSchema,
            output_schema=GetScorecardsToolResponse,
            function=self.get_scorecards,
        )
        self.port_client = port_client

    async def get_scorecards(self, props: GetScorecardsToolSchema) -> Dict[str, Any]:
        args = props.dict()
        blueprint_identifier = args.get("blueprint_identifier")
        detailed = args.get("detailed")
        logger.info(f"Retrieving all scorecards from Port (detailed={detailed})")
        scorecards = GetScorecardsToolResponse(scorecards=await self.port_client.get_all_scorecards(blueprint_identifier))
        return scorecards.dict()