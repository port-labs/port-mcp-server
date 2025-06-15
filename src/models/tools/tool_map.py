from dataclasses import dataclass, field

import mcp.types as types

import src.tools as mcp_tools
from src.client.client import PortClient
from src.models.tools.tool import Tool
from src.tools.action.dynamic_actions import DynamicActionToolsManager
from src.utils import logger


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
        self._register_dynamic_action_tools()

    def _register_dynamic_action_tools(self) -> None:
        """Register dynamic tools for each Port action."""
        try:
            dynamic_manager = DynamicActionToolsManager(self.port_client)
            dynamic_tools = dynamic_manager.get_dynamic_action_tools_sync()

            for tool in dynamic_tools:
                self.register_tool(tool)

            logger.info(f"Registered {len(dynamic_tools)} dynamic action tools")
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
