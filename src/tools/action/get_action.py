from typing import Any

from pydantic import Field

from src.client import PortClient
from src.models.actions.action import Action
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool
from src.utils import logger


class GetActionToolSchema(BaseModel):
    action_identifier: str = Field(..., description="The identifier of the action to get")


class GetActionTool(Tool[GetActionToolSchema]):
    """Get detailed information for a specific action"""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_action",
            description="Get detailed information for a specific action using its identifier",
            input_schema=GetActionToolSchema,
            output_schema=Action,
            annotations=Annotations(
                title="Get Action",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.get_action,
        )
        self.port_client = port_client

    async def get_action(self, props: GetActionToolSchema) -> dict[str, Any]:
        logger.info(f"GetActionTool.get_action called with props: {props}")

        action = await self.port_client.get_action(props.action_identifier)

        return action.model_dump(exclude_unset=True, exclude_none=True)
