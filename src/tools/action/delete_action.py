from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool


class DeleteActionToolSchema(BaseModel):
    action_identifier: str = Field(..., description="The identifier of the action to delete")


class DeleteActionToolResponse(BaseModel):
    success: bool = Field(..., description="Whether the action was deleted successfully")
    message: str = Field(..., description="The message from the operation")


class DeleteActionTool(Tool[DeleteActionToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="delete_action",
            description="Delete a self-service action or automation. To learn more about actions and automations, check out the documentation at https://docs.port.io/actions-and-automations/",
            input_schema=DeleteActionToolSchema,
            output_schema=DeleteActionToolResponse,
            annotations=Annotations(
                title="Delete Action",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True,
            ),
            function=self.delete_action,
        )
        self.port_client = port_client

    async def delete_action(self, props: DeleteActionToolSchema) -> dict[str, Any]:
        args = props.model_dump()
        action_identifier = args.get("action_identifier")

        if not action_identifier:
            raise ValueError("Action identifier is required")

        result = await self.port_client.delete_action(action_identifier)
        return {"success": result, "message": f"Action '{action_identifier}' deleted successfully"}