from typing import Any

from src.client.client import PortClient
from src.models.actions import Action, ActionCreate
from src.models.common.annotations import Annotations
from src.models.tools.tool import Tool


class CreateActionToolSchema(ActionCreate):
    pass


class CreateActionTool(Tool[CreateActionToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="create_action",
            description="Create a new self-service action or automation in your Port account. To learn more about actions and automations, check out the documentation at https://docs.port.io/actions-and-automations/",
            function=self.create_action,
            input_schema=CreateActionToolSchema,
            output_schema=Action,
            annotations=Annotations(
                title="Create Action",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True,
            ),
        )
        self.port_client = port_client

    async def create_action(self, props: CreateActionToolSchema) -> dict[str, Any]:
        """
        Create a new action or automation.
        """
        action_data = props.model_dump(exclude_none=True, exclude_unset=True)

        created_action = await self.port_client.create_action(action_data)
        created_action_dict = created_action.model_dump(exclude_unset=True, exclude_none=True)

        return created_action_dict