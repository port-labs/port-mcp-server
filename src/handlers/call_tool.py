import json
from typing import Any

from loguru import logger
from mcp.types import TextContent
from pydantic import ValidationError

from src.models.tools import Tool


async def execute_tool(tool: Tool, arguments: dict[str, Any]):
    tool_name = tool.name
    logger.info(f"Executing tool {tool_name}")
    logger.debug(f"Executing tool {tool_name} with arguments: {arguments}")
    try:
        validated_args = tool.validate_input(arguments)
        logger.debug("Validation was successful")
        result = await tool.function(validated_args)
        result_str = json.dumps(result)
        logger.debug(f"Tool {tool_name} returned: {result_str}")
        return [TextContent(type="text", text=result_str)]
    except ValidationError as e:
        errors = e.errors()
        logger.error(f"Error calling tool {tool_name}: {errors}, {e}")
        raise Exception(f"Error calling tool {tool_name}: {errors}") from e
    except Exception as e:
        logger.exception(f"Error calling tool {tool_name}: {e}")
        raise Exception(f"Error calling tool {tool_name}: {e}") from e
