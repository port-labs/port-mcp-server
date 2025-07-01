import json
from typing import Any

from pydantic import field_validator, model_validator

from src.client.client import PortClient
from src.models.actions import Action, ActionCreate
from src.models.actions.action import ActionInvocationMethod
from src.models.common.annotations import Annotations
from src.models.tools.tool import Tool


class CreateActionToolSchema(ActionCreate):
    @field_validator('invocation_method', mode='before')
    @classmethod
    def parse_invocation_method(cls, v) -> ActionInvocationMethod | dict:
        """Parse invocation method if it's provided as a JSON string."""
        if isinstance(v, str):
            try:
                # Parse the JSON string into a dictionary
                parsed = json.loads(v)
                return parsed
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON string for invocationMethod: {e}") from e
        return v

    @model_validator(mode='before')
    @classmethod
    def handle_invocation_method_alias(cls, values):
        """Handle both invocationMethod and invocation_method field names."""
        if isinstance(values, dict) and 'invocationMethod' in values and isinstance(values['invocationMethod'], str):
            # If invocationMethod is provided as a string, parse it
            try:
                values['invocationMethod'] = json.loads(values['invocationMethod'])
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON string for invocationMethod: {e}") from e
        return values


class CreateActionTool(Tool[CreateActionToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="create_action",
            description="Create a new self-service action.",
            function=self.create_action,
            input_schema=CreateActionToolSchema,
            output_schema=Action,
            annotations=Annotations(
                title="Create Action",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True,
            ),
        )
        self.port_client = port_client

    async def create_action(self, props: CreateActionToolSchema) -> dict[str, Any]:
        """
        Create a new action or automation.
        """
        action_data = props.model_dump(exclude_none=True, exclude_unset=True)

        created_action = await self.port_client.create_action(action_data)
        created_action_dict = created_action.model_dump(exclude_unset=True, exclude_none=True)

        return created_action_dict
