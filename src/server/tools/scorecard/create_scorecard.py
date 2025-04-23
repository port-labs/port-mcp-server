from pydantic import Field
from loguru import logger
from src.server.models import Scorecard, ScorecardCreate, Annotations
from src.server.models.tools.tool import Tool
from src.server.client.client import PortClient
from typing import Any, Dict

class CreateScorecardToolSchema(ScorecardCreate):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to create the scorecard for")
class CreateScorecardTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="create_scorecard",
            description="Create scorecards to define and track metrics/standards for our Port entities, based on their properties",
            function=self.create_scorecard,
            input_schema=CreateScorecardToolSchema,
            output_schema=Scorecard,
            annotations=Annotations(
                title="Create Scorecard",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True
            ),
        )
        self.port_client = port_client

    async def create_scorecard(
        self,
        props: CreateScorecardToolSchema
    ) -> Dict[str, Any]:
        """
        Create a new scorecard for a specific blueprint.
        """
        args = props.model_dump()
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
                    return f"❌ Error creating scorecard: The base level '{base_level}' cannot have rules associated with it."
        
        logger.info(f"Creating scorecard '{identifier}' for blueprint '{blueprint_identifier}'")
        logger.debug(f"Scorecard data: {props}")
        
        # Convert dataclass to dict for API            
        # Create the scorecard
        scorecard_data = props.model_dump(exclude_none=True,exclude_unset=True)
        #remove the blueprint_identifier from the scorecard_data
        scorecard_data.pop("blueprint_identifier")
        created_scorecard = await self.port_client.create_scorecard(blueprint_identifier, scorecard_data)
        created_scorecard_dict = created_scorecard.model_dump(exclude_unset=True, exclude_none=True)
        return created_scorecard_dict