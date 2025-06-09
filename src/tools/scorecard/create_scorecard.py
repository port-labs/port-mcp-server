from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.scorecards import Scorecard, ScorecardCreate
from src.models.tools.tool import Tool
from src.utils import logger


class CreateScorecardToolSchema(ScorecardCreate):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to create the scorecard for")


class CreateScorecardTool(Tool[CreateScorecardToolSchema]):
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
                openWorldHint=True,
            ),
        )
        self.port_client = port_client

    async def create_scorecard(self, props: CreateScorecardToolSchema) -> dict[str, Any]:
        """
        Create a new scorecard for a specific blueprint.
        """
        args = props.model_dump()
        blueprint_identifier = args.get("blueprint_identifier")
        levels = args.get("levels")
        rules = args.get("rules")

        # Validate that rules don't reference the first level (base level)
        if rules and levels and isinstance(levels, list) and len(levels) > 0:
            base_level = levels[0]
            base_level_title = base_level.get("title")
            for rule in rules:
                rule_level = rule.get("level")
                if rule_level == base_level_title:
                    message = (
                        f"❌ Error creating scorecard: The base level '{base_level_title}' cannot have rules associated with it."
                    )
                    logger.error(message)
                    raise Exception(message)

        scorecard_data = props.model_dump(exclude_none=True, exclude_unset=True)
        scorecard_data.pop("blueprint_identifier")

        if not blueprint_identifier:
            raise ValueError("Blueprint identifier is required")

        created_scorecard = await self.port_client.create_scorecard(blueprint_identifier, scorecard_data)
        created_scorecard_dict = created_scorecard.model_dump(exclude_unset=True, exclude_none=True)
        return created_scorecard_dict
