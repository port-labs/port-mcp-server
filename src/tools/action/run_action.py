from typing import Any
from pydantic import Field

from src.client import PortClient
from src.models.action_run.action_run import ActionRun
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool
from pydantic.json_schema import SkipJsonSchema


class RunActionToolSchema(BaseModel):
    action_identifier: str = Field(description="The identifier of the action to run")
    entity_identifier: str | SkipJsonSchema[None] = Field(
        default=None,
        description="Optional entity identifier if action is entity-specific, if the action contains blueprint and the type is DAY-2 or DELETE, create does not require an entity identifier",
    )
    blueprint_identifier: str | SkipJsonSchema[None] = Field(
        default=None,
        description="Optional blueprint identifier if action is blueprint-specific, if the action contains blueprint in the actions schema",
    )
    properties: dict | SkipJsonSchema[None] = Field(
        default=None,
        description="Action properties based on the actions trigger.userInputs schema",
    )


class RunActionToolResponse(BaseModel):
    action_run: ActionRun = Field(description="Action run details including run_id for tracking")
    ui_link: str = Field(description="Direct link to view the action run in Port UI")


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
        run_payload = {}
        if props.properties:
            run_payload["properties"] = props.properties

        if not self.port_client.action_runs:
            raise ValueError("Action runs client not available")

        if props.entity_identifier and props.blueprint_identifier:
            action_run = await self.port_client.create_entity_action_run(
                blueprint_identifier=props.blueprint_identifier,
                entity_identifier=props.entity_identifier,
                action_identifier=props.action_identifier,
                **run_payload,
            )
        elif props.blueprint_identifier:
            action_run = await self.port_client.create_blueprint_action_run(
                blueprint_identifier=props.blueprint_identifier,
                action_identifier=props.action_identifier,
                **run_payload,
            )
        else:
            action_run = await self.port_client.create_global_action_run(
                action_identifier=props.action_identifier, **run_payload
            )

        # Generate the UI link for the action run
        ui_link = f"https://app.getport.io/organization/run?runId={action_run.id}"

        response = RunActionToolResponse.construct(action_run=action_run, ui_link=ui_link)
        return response.model_dump(exclude_unset=True, exclude_none=True)
