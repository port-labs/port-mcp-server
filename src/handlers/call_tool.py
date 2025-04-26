import json
from typing import Any, Dict

from loguru import logger
from mcp.types import TextContent
from pydantic import ValidationError

from src.models.tools import Tool


async def execute_tool(tool: Tool, arguments: Dict[str, Any]):
    tool_name = tool.name
    logger.info(f"Executing tool {tool_name}")
    logger.debug(f"Executing tool {tool_name} with arguments: {arguments}")
    try:
        validated_args = tool.validate_input(arguments)
        logger.debug(f"Validation was successful")
        result = await tool.function(validated_args)
        logger.debug(f"Tool {tool_name} returned: {result}")
        return [TextContent(type="text", text=json.dumps(result))]
    except ValidationError as e:
        errors = e.errors()
        logger.error(f"Error calling tool {tool_name}: {errors}, {e}")
        raise Exception(f"Error calling tool {tool_name}: {errors}") from e
    except Exception as e:
        logger.exception(f"Error calling tool {tool_name}: {e}")
        raise Exception(f"Error calling tool {tool_name}: {e}") from e
