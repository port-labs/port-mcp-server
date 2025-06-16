from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.actions import Action, ActionUpdate
from src.models.common.annotations import Annotations
from src.models.tools.tool import Tool


class UpdateActionToolSchema(ActionUpdate):
    action_identifier: str = Field(..., description="The identifier of the action to update")


class UpdateActionTool(Tool[UpdateActionToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_action",
            description="Update an existing self-service action or automation in your Port account. To learn more about actions and automations, check out the documentation at https://docs.port.io/actions-and-automations/",
            function=self.update_action,
            input_schema=UpdateActionToolSchema,
            output_schema=Action,
            annotations=Annotations(
                title="Update Action",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True,
            ),
        )
        self.port_client = port_client

    async def update_action(self, props: UpdateActionToolSchema) -> dict[str, Any]:
        args = props.model_dump()
        action_identifier = args.get("action_identifier")
        action_data = props.model_dump(exclude_none=True, exclude_unset=True)
        action_data.pop("action_identifier")

        if not action_identifier:
            raise ValueError("Action identifier is required")

        updated_action = await self.port_client.update_action(action_identifier, action_data)
        updated_action_dict = updated_action.model_dump(exclude_unset=True, exclude_none=True)

        return updated_action_dict