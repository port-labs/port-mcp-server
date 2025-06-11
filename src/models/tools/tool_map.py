"""
Tool map for managing MCP tools.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
import asyncio

import mcp.types as types
from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

import src.tools as mcp_tools
from src.client.client import PortClient
from src.models.actions.action import Action
from src.models.action_run.action_run import ActionRun
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel as PortBaseModel
from src.models.tools.tool import Tool
from src.utils import logger

class DynamicActionToolSchema(BaseModel):
    """Simple schema for dynamic action tools."""
    entity_identifier: str | SkipJsonSchema[None] = Field(
        default=None,
        description="Optional entity identifier if action is entity-specific, if the action contains blueprint and the type is DAY-2 or DELETE, create an entity first and pass the identifier here"
    )
    properties: dict[str, Any] | SkipJsonSchema[None] = Field(
        default=None,
        description="Properties for the action. To see required properties, first call get_action with action_identifier to view the userInputs schema."
    )


class DynamicActionToolResponse(PortBaseModel):
    """Response model for dynamic action tools."""
    action_run: ActionRun = Field(description="Action run details including run_id for tracking")


def _camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


@dataclass
class ToolMap:
    port_client: PortClient
    tools: dict[str, Tool] = field(default_factory=dict)

    def __post_init__(self):
        # Register static tools
        for tool in mcp_tools.__all__:
            module = mcp_tools.__dict__[tool]
            self.register_tool(module(self.port_client))
        logger.info(f"ToolMap initialized with {len(self.tools)} static tools")
        
        # Register dynamic action tools if enabled
        from src.config import config
        if config.dynamic_actions_enabled:
            self._register_dynamic_action_tools()

    def _create_dynamic_action_tool(self, action: Action) -> Tool:
        """Create a dynamic tool for a specific Port action."""
        
        # Create the tool function
        async def dynamic_action_function(props: DynamicActionToolSchema) -> dict[str, Any]:
            if not self.port_client.action_runs:
                raise ValueError("Action runs client not available")

            # Execute the action
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

        # Create tool name (limited to 40 chars for server prefix)
        base_tool_name = f"run_{_camel_to_snake(action.identifier)}"
        tool_name = base_tool_name[:40] if len(base_tool_name) > 40 else base_tool_name
        
        # Create tool description
        description = f"Execute the '{action.title}' action"
        if action.description:
            description += f": {action.description}"
        description += f"\n\nTo see required properties, first call get_action with action_identifier='{action.identifier}' to view the userInputs schema."
        
        # Create and return the tool
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

    def _register_dynamic_action_tools(self) -> None:
        """Register dynamic tools for each Port action."""
        try:
            from src.tools.action.list_actions import ListActionsTool, ListActionsToolSchema
            from src.tools.action.get_action import GetActionTool, GetActionToolSchema

            # Get all actions - call the async function properly
            list_actions_tool = ListActionsTool(self.port_client)
            actions_response = asyncio.run(list_actions_tool.list_actions(ListActionsToolSchema()))
            actions = actions_response.get("actions", [])
            
            # Get detailed action info and create tools
            get_action_tool = GetActionTool(self.port_client)
            dynamic_tools_count = 0
            
            for action_data in actions:
                try:
                    # Handle both dict and ActionSummary objects
                    action_identifier = action_data.get("identifier") if isinstance(action_data, dict) else action_data.identifier
                    
                    # Get full action details - call the async function properly
                    action_response = asyncio.run(get_action_tool.get_action(GetActionToolSchema(action_identifier=action_identifier)))
                    
                    # Use parse_obj_as with validation disabled to avoid Pydantic warnings
                    action = Action.model_validate(action_response, strict=False)
                    
                    if action:
                        # Create and register dynamic tool
                        dynamic_tool = self._create_dynamic_action_tool(action)
                        self.register_tool(dynamic_tool)
                        dynamic_tools_count += 1
                        
                except Exception as e:
                    logger.warning(f"Failed to create dynamic tool for action {action_identifier}: {e}")
                    continue
            
            logger.info(f"Registered {dynamic_tools_count} dynamic action tools")
            
        except Exception as e:
            logger.error(f"Failed to register dynamic action tools: {e}")

    def list_tools(self) -> list[types.Tool]:
        return [
            types.Tool(
                name=tool.name,
                description=tool.description,
                inputSchema=tool.input_schema_json,
                annotations=tool.annotations.model_dump(),  # type: ignore
            )
            for tool in self.tools.values()
        ]

    def get_tool(self, tool_name: str) -> Tool:
        try:
            tool = self.tools[tool_name]
            logger.info(f"Got tool: {tool_name}, {tool}")
            return tool
        except KeyError:
            error_msg = f"Tool not found: {tool_name}"
            logger.error(error_msg)
            raise ValueError(error_msg) from None

    def get_tools(self, tool_names: list[str] | None = None) -> list[Tool]:
        if tool_names is None:
            return list(self.tools.values())
        return [self.get_tool(tool_name) for tool_name in tool_names]

    def register_tool(self, tool: Tool) -> None:
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    async def get_tool_with_dynamic_loading(self, tool_name: str) -> Tool:
        """Get tool with support for dynamic loading if needed."""
        return self.get_tool(tool_name)
