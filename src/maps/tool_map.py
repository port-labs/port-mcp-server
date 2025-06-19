from src.client import PortClient
from src.config import get_config
from src.models.tools import ToolMap
from src.utils import logger


def init_tool_map() -> ToolMap:
    config = get_config()
    logger.info(f"Initializing tool map with config region: {config.region}")
    logger.debug(f"Client ID available: {bool(config.port_client_id)}")
    logger.debug(f"Client secret available: {bool(config.port_client_secret)}")
    
    port_client = PortClient(
        client_id=config.port_client_id,
        client_secret=config.port_client_secret,
        region=config.region,
    )
    logger.info("PortClient created successfully")
    
    tool_map = ToolMap(port_client=port_client)
    logger.info("Tool map created, initializing tools...")
    logger.debug(f"Tool map: {tool_map}")
    return tool_map


tool_map: ToolMap | None = None


def get_tool_map() -> ToolMap:
    """Get the global tool map, initializing it if necessary."""
    global tool_map
    if tool_map is None:
        tool_map = init_tool_map()
    return tool_map
