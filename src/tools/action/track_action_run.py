import asyncio
from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.action_run import ActionRun
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool


class TrackActionRunToolSchema(BaseModel):
    run_id: str = Field(description="The action run ID to track")
    poll_interval: int = Field(default=2, description="How often to poll for updates (seconds)")


class TrackActionRunToolResponse(BaseModel):
    action_run: ActionRun = Field(description="Final action run status and details")


class TrackActionRunTool(Tool[TrackActionRunToolSchema]):
    """Track an action run's progress and show logs"""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="track_action_run",
            description="Track an action run's progress, showing logs and final status",
            input_schema=TrackActionRunToolSchema,
            output_schema=TrackActionRunToolResponse,
            annotations=Annotations(
                title="Track Action Run Progress",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=False,
            ),
            function=self.track_action_run,
        )
        self.port_client = port_client

    async def track_action_run(self, props: TrackActionRunToolSchema) -> dict[str, Any]:
        action_run = await self.port_client.get_action_run(props.run_id)

        while True:
            action_run = await self.port_client.get_action_run(props.run_id)

            status = action_run.status

            if status in ["SUCCESS", "FAILURE", "CANCELLED"]:
                response = TrackActionRunToolResponse.construct(action_run=action_run)
                return response.model_dump(exclude_unset=True, exclude_none=True)

            # Wait before next poll
            await asyncio.sleep(props.poll_interval)
