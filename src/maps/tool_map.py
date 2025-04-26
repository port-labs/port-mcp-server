from typing import Any

from loguru import logger
from src.client import PortClient
from src.models.tools import ToolMap
from src.config import config

def init_tool_map() -> ToolMap:
    port_client = PortClient(
        client_id=config.port_client_id,
        client_secret=config.port_client_secret,
        region=config.region,
    )
    tool_map = ToolMap(port_client=port_client)
    logger.info("Initialized tool map")
    logger.debug(f"Tool map: {tool_map}")
    return tool_map

tool_map: ToolMap = init_tool_map()