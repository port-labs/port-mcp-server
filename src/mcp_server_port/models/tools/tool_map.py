from dataclasses import field, dataclass
import mcp.types as types
from loguru import logger
from src.mcp_server_port.models.tools.tool import Tool
from src.mcp_server_port.models.common import Singleton

@dataclass
class ToolMap(metaclass=Singleton):
    tools: dict[str, Tool] = field(default_factory=dict)
    
    def list_tools(self) -> list[types.Tool]:
        tools = [types.Tool(name=tool.name, description=tool.description, inputSchema=tool.inputSchema) for tool in self.tools.values()]
        logger.info(f"Tool list: {tools}")
        return tools
    def get_tool(self, tool_name: str) -> Tool:
        tool = self.tools[tool_name]
        logger.info(f"Got tool: {tool_name}, {tool}")
        return tool
    def register_tool(self, tool: Tool) -> None:
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")