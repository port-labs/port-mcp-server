from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.blueprints import Blueprint
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool


class GetBlueprintsToolSchema(BaseModel):
    detailed: bool = Field(default=True, description="Whether to return detailed blueprints")


class GetBlueprintsToolResponse(BaseModel):
    blueprints: list[Blueprint] = Field(description="The list of blueprints")


class GetBlueprintsTool(Tool[GetBlueprintsToolSchema]):
    """Get blueprints from Port"""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_blueprints",
            description="Get all of the blueprints in your organization",
            input_schema=GetBlueprintsToolSchema,
            output_schema=GetBlueprintsToolResponse,
            annotations=Annotations(
                title="Get Blueprints",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.get_blueprints,
        )
        self.port_client = port_client

    async def get_blueprints(self, props: GetBlueprintsToolSchema) -> dict[str, Any]:
        blueprints = await self.port_client.get_blueprints()
        response = GetBlueprintsToolResponse.construct(blueprints=blueprints)
        return response.model_dump(exclude_unset=True, exclude_none=True)
