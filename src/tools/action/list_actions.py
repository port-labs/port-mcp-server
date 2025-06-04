from typing import Any, Optional

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool


class ListActionsToolSchema(BaseModel):
    blueprint_identifier: Optional[str] = Field(
        default=None, 
        description="Optional blueprint identifier to filter actions for a specific blueprint"
    )


class ListActionsToolResponse(BaseModel):
    actions: list[dict] = Field(description="The list of available actions")


class ListActionsTool(Tool):
    """List available actions in Port"""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="list_actions",
            description="Get all available actions in Port, optionally filtered by blueprint",
            input_schema=ListActionsToolSchema,
            output_schema=ListActionsToolResponse,
            annotations=Annotations(
                title="List Actions",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.list_actions,
        )
        self.port_client = port_client

    async def list_actions(self, props: ListActionsToolSchema) -> dict[str, Any]:
        # Use PyPort's actions API
        if props.blueprint_identifier:
            actions = await self.port_client.actions.get_blueprint_actions(props.blueprint_identifier)
        else:
            actions = await self.port_client.actions.get_all_actions()
        
        response = ListActionsToolResponse.construct(actions=actions)
        return response.model_dump(exclude_unset=True, exclude_none=True) 