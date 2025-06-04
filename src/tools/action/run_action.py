from typing import Any, Optional

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool


class RunActionToolSchema(BaseModel):
    action_identifier: str = Field(description="The identifier of the action to run")
    entity_identifier: Optional[str] = Field(
        default=None, 
        description="Optional entity identifier if action is entity-specific"
    )
    blueprint_identifier: Optional[str] = Field(
        default=None, 
        description="Optional blueprint identifier if action is blueprint-specific"
    )
    properties: Optional[dict] = Field(
        default=None, 
        description="Optional action input properties"
    )


class RunActionToolResponse(BaseModel):
    action_run: dict = Field(description="Action run details including run_id for tracking")


class RunActionTool(Tool):
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
        # Prepare the action run payload
        run_payload = {}
        if props.properties:
            run_payload["properties"] = props.properties
        
        # Use PyPort's action runs API
        if props.entity_identifier:
            # Entity-specific action
            action_run = await self.port_client.action_runs.create_entity_action_run(
                blueprint_identifier=props.blueprint_identifier,
                entity_identifier=props.entity_identifier,
                action_identifier=props.action_identifier,
                **run_payload
            )
        elif props.blueprint_identifier:
            # Blueprint-specific action
            action_run = await self.port_client.action_runs.create_blueprint_action_run(
                blueprint_identifier=props.blueprint_identifier,
                action_identifier=props.action_identifier,
                **run_payload
            )
        else:
            # Global action
            action_run = await self.port_client.action_runs.create_global_action_run(
                action_identifier=props.action_identifier,
                **run_payload
            )
        
        response = RunActionToolResponse.construct(action_run=action_run)
        return response.model_dump(exclude_unset=True, exclude_none=True) 