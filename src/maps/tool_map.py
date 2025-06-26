from src.client import PortClient
from src.config import get_config
from src.models.tools import ToolMap
from src.utils import logger


def init_tool_map() -> ToolMap:
    config = get_config()
    port_client = PortClient(
        client_id=config.port_client_id,
        client_secret=config.port_client_secret,
        region=config.region,
    )
    tool_map = ToolMap(port_client=port_client)
    logger.info("Initialized tool map")
    logger.debug(f"Tool map: {tool_map}")
    return tool_map


# Delay initialization until needed
tool_map: ToolMap | None = None


def get_tool_map() -> ToolMap:
    """Get the tool map, initializing if needed."""
    global tool_map
    if tool_map is None:
        tool_map = init_tool_map()
    return tool_map
