from typing import Any

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.client import PortClient
from src.models.action_run.action_run import ActionRun
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool


class RunActionToolSchema(BaseModel):
    action_identifier: str = Field(description="The identifier of the action to run")
    entity_identifier: str | SkipJsonSchema[None] = Field(
        default=None,
        description="Optional entity identifier if action is entity-specific, if the action contains blueprint and the type is DAY-2 or DELETE, create does not require an entity identifier",
    )
    properties: dict | SkipJsonSchema[None] = Field(
        default=None,
        description="Action properties based on the actions trigger.userInputs schema",
    )


class RunActionToolResponse(BaseModel):
    action_run: ActionRun = Field(description="Action run details including run_id for tracking")


class RunActionTool(Tool[RunActionToolSchema]):
    """Run a Port action"""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="run_action",
            description="Run a Port action and return the action run details for tracking",
            input_schema=RunActionToolSchema,
            output_schema=RunActionToolResponse,
            annotations=Annotations(
                title="Run Action",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=False,
            ),
            function=self.run_action,
        )
        self.port_client = port_client

    async def run_action(self, props: RunActionToolSchema) -> dict[str, Any]:
        run_payload: dict[str, Any] = {}
        if props.properties:
            run_payload["properties"] = props.properties
        else:
            run_payload["properties"] = {}

        if not self.port_client.action_runs:
            raise ValueError("Action runs client not available")

        if props.entity_identifier:
            run_payload["entity"] = props.entity_identifier
            action_run = await self.port_client.create_entity_action_run(
                action_identifier=props.action_identifier,
                **run_payload,
            )
        else:
            action_run = await self.port_client.create_global_action_run(
                action_identifier=props.action_identifier, **run_payload
            )

        response = RunActionToolResponse.construct(action_run=action_run)
        return response.model_dump(exclude_unset=True, exclude_none=True)
