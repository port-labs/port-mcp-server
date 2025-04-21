from pydantic import Field
from loguru import logger
from src.mcp_server_port.models.tools import Tool
from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.scorecards import Scorecard, ScorecardCreate
from typing import Any, Dict

class UpdateScorecardToolSchema(ScorecardCreate):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to create the scorecard for")
    scorecard_identifier: str = Field(..., description="The identifier of the scorecard to update")
class UpdateScorecardTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_scorecard",
            description="Update a scorecard for a specific blueprint using it's identifier",
            function=self.update_scorecard,
            input_schema=UpdateScorecardToolSchema,
            output_schema=Scorecard,
        )
        self.port_client = port_client

    async def update_scorecard(
        self,
        props: UpdateScorecardToolSchema
    ) -> Dict[str, Any]:
        """
        Update a scorecard for a specific blueprint.
        """
        args = props.dict()
        blueprint_identifier = args.get("blueprint_identifier")
        identifier = args.get("identifier")
        title = args.get("title")
        levels = args.get("levels")
        rules = args.get("rules")
        description = args.get("description")
            # Validate that rules don't reference the first level (base level)
        if rules and len(levels) > 0:
            base_level = levels[0]
            for rule in rules:
                if rule.get("level") == base_level.get("title"):
                    return f"❌ Error updating scorecard: The base level '{base_level}' cannot have rules associated with it."
        
        logger.info(f"Updating scorecard '{identifier}' for blueprint '{blueprint_identifier}'")
        logger.debug(f"Scorecard data: {props}")
        
        # Convert dataclass to dict for API            
        # Create the scorecard
        scorecard_data = props.dict(exclude_none=True,exclude_unset=True)
        #remove the blueprint_identifier from the scorecard_data
        scorecard_data.pop("blueprint_identifier")
        scorecard_data.pop("scorecard_identifier")
        created_scorecard = await self.port_client.update_scorecard(blueprint_identifier, scorecard_data)
    
        # Return the created scorecard details
        return created_scorecard.dict(exclude_unset=True, exclude_none=True)