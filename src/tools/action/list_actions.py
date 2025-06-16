from typing import Any

from pydantic import Field

from src.client import PortClient
from src.models.actions.action import ActionSummary
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool
from src.utils import logger


class ListActionsToolSchema(BaseModel):
    detailed: bool = Field(default=True, description="Whether to return detailed actions")
    trigger_type: str = Field(
        default="self-service",
        description="The type of trigger to filter actions by self-service or automation",
    )


class ListActionsToolResponse(BaseModel):
    actions: list[ActionSummary] = Field(description="The list of available actions with basic information")


class ListActionsTool(Tool[ListActionsToolSchema]):
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
        logger.info(f"ListActionsTool.list_actions called with props: {props}")

        actions = await self.port_client.get_all_actions(props.trigger_type)

        # Convert full Action objects to ActionSummary objects
        action_summaries = [
            ActionSummary(
                identifier=action.identifier,
                title=action.title,
                description=action.description,
                blueprint=getattr(action.trigger, 'blueprint_identifier', None),
            )
            for action in actions
        ]

        response = ListActionsToolResponse(actions=action_summaries)
        return response.model_dump(exclude_unset=True, exclude_none=True)
