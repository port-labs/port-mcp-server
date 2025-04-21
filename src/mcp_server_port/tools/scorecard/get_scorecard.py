from loguru import logger
from src.mcp_server_port.models.scorecards import Scorecard
from src.mcp_server_port.models.tools import Tool
from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field
from typing import Any, Dict

class GetScorecardToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get scorecard for")
    scorecard_identifier: str = Field(..., description="The identifier of the scorecard to get")
    detailed: bool = Field(default=True, description="If True (default), returns complete scorecard details including rules and calculation method. If False, returns summary information only.")
class GetScorecardTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_scorecard",
            description="Get a specific scorecard for a given blueprint using it's identifier",
            input_schema=GetScorecardToolSchema,
            output_schema=Scorecard,
            function=self.get_scorecard,
        )
        self.port_client = port_client

    async def get_scorecard(self, props: GetScorecardToolSchema) -> Dict[str, Any]:
  
            args = props.dict()
            scorecard_identifier = args.get("scorecard_identifier")
            blueprint_identifier = args.get("blueprint_identifier")
            detailed = args.get("detailed")
            
            logger.info(f"Retrieving scorecard '{scorecard_identifier}' (detailed={detailed})")
            
            if blueprint_identifier:
                logger.info(f"Blueprint ID provided: {blueprint_identifier}")
                
            scorecard = await self.port_client.get_scorecard_details(scorecard_identifier, blueprint_identifier)
            return scorecard.dict(exclude_unset=True, exclude_none=True)
    