from typing import Any, Dict
from pydantic import Field, BaseModel
from pydantic.json_schema import SkipJsonSchema

from src.client import PortClient
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


def create_dynamic_action_tool(action: Action, port_client: PortClient) -> Tool:
    """Create a dynamic tool for a specific Port action."""
    
    # Create the tool function
    async def dynamic_action_function(props: DynamicActionToolSchema) -> dict[str, Any]:
        if not port_client.action_runs:
            raise ValueError("Action runs client not available")

        # Execute the action
        if props.entity_identifier:
            action_run = await port_client.create_entity_action_run(
                action_identifier=action.identifier,
                entity=props.entity_identifier,
                properties=props.properties or {},
            )
        else:
            action_run = await port_client.create_global_action_run(
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
        response_schema=DynamicActionToolResponse,
        annotations=Annotations(),
    ) 