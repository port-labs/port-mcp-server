"""
Dynamic action tools for Port MCP server.

This module provides functionality to dynamically create tools for Port actions.
"""

import asyncio
import re
from typing import Any

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from src.client.client import PortClient
from src.models.action_run.action_run import ActionRun
from src.models.actions.action import Action
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel as PortBaseModel
from src.models.tools.tool import Tool
from src.tools.action.get_action import GetActionTool, GetActionToolSchema
from src.tools.action.list_actions import ListActionsTool, ListActionsToolSchema
from src.utils import logger


class DynamicActionToolSchema(BaseModel):
    """Simple schema for dynamic action tools."""

    entity_identifier: str | SkipJsonSchema[None] = Field(
        default=None,
        description="Optional entity identifier if action is entity-specific, if the action contains blueprint and the type is DAY-2 or DELETE, create an entity first and pass the identifier here",
    )
    properties: dict[str, Any] | SkipJsonSchema[None] = Field(
        default=None,
        description="Properties for the action. To see required properties, first call get_action with action_identifier to view the userInputs schema.",
    )


class DynamicActionToolResponse(PortBaseModel):
    """Response model for dynamic action tools."""

    action_run: ActionRun = Field(description="Action run details including run_id for tracking")


def _camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class DynamicActionToolsManager:
    """Manager for creating and registering dynamic action tools."""

    def __init__(self, port_client: PortClient):
        self.port_client = port_client

    def _create_dynamic_action_tool(self, action: Action) -> Tool:
        """Create a dynamic tool for a specific Port action."""

        async def dynamic_action_function(props: DynamicActionToolSchema) -> dict[str, Any]:
            if not self.port_client.action_runs:
                raise ValueError("Action runs client not available")

            if props.entity_identifier:
                action_run = await self.port_client.create_entity_action_run(
                    action_identifier=action.identifier,
                    entity=props.entity_identifier,
                    properties=props.properties or {},
                )
            else:
                action_run = await self.port_client.create_global_action_run(
                    action_identifier=action.identifier,
                    properties=props.properties or {},
                )

            return DynamicActionToolResponse(action_run=action_run).model_dump()

        base_tool_name = f"run_{_camel_to_snake(action.identifier)}"
        tool_name = base_tool_name[:40] if len(base_tool_name) > 40 else base_tool_name

        description = f"Execute the '{action.title}' action"
        if action.description:
            description += f": {action.description}"
        description += f"\n\nTo see required properties, first call get_action with action_identifier='{action.identifier}' to view the userInputs schema."

        return Tool(
            name=tool_name,
            description=description,
            function=dynamic_action_function,
            input_schema=DynamicActionToolSchema,
            output_schema=DynamicActionToolResponse,
            annotations=Annotations(
                title=f"Run {action.title}",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True,
            ),
        )

    async def get_dynamic_action_tools(self) -> list[Tool]:
        """Get all dynamic action tools by fetching actions from Port."""
        tools = []
        try:
            list_actions_tool = ListActionsTool(self.port_client)
            actions_response = await list_actions_tool.list_actions(ListActionsToolSchema())
            actions = actions_response.get("actions", [])

            get_action_tool = GetActionTool(self.port_client)

            for action_data in actions:
                try:
                    action_identifier = (
                        action_data.get("identifier")
                        if isinstance(action_data, dict)
                        else action_data.identifier
                    )

                    if not action_identifier:
                        logger.warning("Skipping action with no identifier")
                        continue

                    action_response = await get_action_tool.get_action(
                        GetActionToolSchema(action_identifier=str(action_identifier))
                    )

                    action = Action.model_validate(action_response, strict=False)

                    if action:
                        dynamic_tool = self._create_dynamic_action_tool(action)
                        tools.append(dynamic_tool)

                except Exception as e:
                    logger.warning(
                        f"Failed to create dynamic tool for action {action_identifier}: {e}"
                    )
                    continue

            logger.info(f"Created {len(tools)} dynamic action tools")

        except Exception as e:
            logger.error(f"Failed to create dynamic action tools: {e}")

        return tools

    def get_dynamic_action_tools_sync(self) -> list[Tool]:
        """Synchronous wrapper for getting dynamic action tools."""
        return asyncio.run(self.get_dynamic_action_tools())
