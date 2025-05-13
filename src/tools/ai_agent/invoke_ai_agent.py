import asyncio
from typing import Any

from pydantic import Field

from src.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.tools.tool import Tool
from src.utils import logger


class InvokeAIAGentToolSchema(BaseModel):
    prompt: str = Field(..., description="The prompt to send to the AI agent")


class InvokeAIAGentToolResponse(BaseModel):
    invocation_id: str = Field(description="The identifier of the invocation")
    invocation_status: str = Field(description="The status of the invocation")
    message: str = Field(description="The message from the AI agent")


class InvokeAIAGentTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="invoke_ai_agent",
            description="Invoke a Port AI agent",
            input_schema=InvokeAIAGentToolSchema,
            output_schema=InvokeAIAGentToolResponse,
            annotations=Annotations(
                title="Invoke AI Agent",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True,
            ),
            function=self.invoke_ai_agent,
        )
        self.port_client = port_client

    async def invoke_ai_agent(self, props: InvokeAIAGentToolSchema) -> dict[str, Any]:
        # Handle both dict input and schema object
        prompt = props.prompt
        # Trigger agent
        logger.info(f"Invoking Port's AI agent with prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
        response = await self.port_client.trigger_agent(prompt)

        # Get identifier from response
        identifier = response.get("invocation", {}).get("identifier")

        if not identifier:
            logger.warning("Could not get invocation identifier from response")
            logger.warning(f"Response data: {response}")
            raise Exception("❌ Error: Could not get invocation identifier from response")

        logger.info(f"Got invocation identifier: {identifier}")

        # Poll for completion
        max_attempts = 10
        attempt = 1
        while attempt < max_attempts:
            logger.info(f"Polling attempt {attempt}/{max_attempts} for invocation {identifier}")
            status = await self.port_client.get_invocation_status(identifier)
            logger.info(f"Status received: {status.status}")

            if status.status.lower() in ["completed", "failed", "error"]:
                logger.info(f"Invocation {identifier} finished with status: {status.status}")
                return InvokeAIAGentToolResponse.construct(
                    invocation_id=identifier, invocation_status=status.status, message=""
                ).model_dump(exclude_unset=True, exclude_none=True)

            logger.warning(f"Invocation {identifier} still in progress after {attempt * 5} seconds. Status: {status.status}")
            logger.warning(f"Status details: {status.__dict__ if hasattr(status, '__dict__') else status}")

            await asyncio.sleep(5)
            attempt += 1

        logger.warning(f"Invocation {identifier} timed out after {max_attempts * 5} seconds")
        logger.warning(f"Last status: {status.status}")
        logger.warning(f"Last status details: {status.__dict__ if hasattr(status, '__dict__') else status}")

        return InvokeAIAGentToolResponse.construct(
            invocation_id=identifier,
            invocation_status="timed_out",
            message="⏳ Operation timed out. You can check the status later with identifier: {identifier}",
        ).model_dump(exclude_unset=True, exclude_none=True)
