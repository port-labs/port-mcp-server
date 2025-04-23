from dataclasses import field, dataclass
import mcp.types as types
from loguru import logger
from src.server.client.client import PortClient

from src.server.models import Singleton
from src.server.models.tools.tool import Tool
import src.server.tools as mcp_tools

@dataclass
class ToolMap():
    port_client: PortClient
    tools: dict[str, Tool] = field(default_factory=dict)
    def __post_init__(self):
        for tool in mcp_tools.__all__:
            module = mcp_tools.__dict__[tool]
            self.register_tool(module(self.port_client))
        logger.info(f"ToolMap initialized with {len(self.tools)} tools")
    def list_tools(self) -> list[types.Tool]:
        tools = [
            types.Tool(
                name=tool.name,
                description=tool.description,
                inputSchema=tool.inputSchema,
                annotations=tool.annotations.dict()
            )
            for tool in self.tools.values()
        ]
        return tools
    def get_tool(self, tool_name: str) -> Tool:
        try:
            tool = self.tools[tool_name]
            logger.info(f"Got tool: {tool_name}, {tool}")
            return tool
        except KeyError:
            error_msg = f"Tool not found: {tool_name}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    def register_tool(self, tool: Tool) -> None:
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")