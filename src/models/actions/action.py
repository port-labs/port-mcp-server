"""Port.io action model."""

from typing import Any

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.models.common.base_pydantic import BaseModel
from src.models.common.icon import Icon


class ActionSchema(BaseModel):
    """Schema for action inputs."""

    properties: dict[str, Any] = Field(
        default_factory=dict, description="Properties schema for action inputs"
    )
    required: list[str] = Field(
        default_factory=list, description="Required properties for the action"
    )


class ActionTrigger(BaseModel):
    """Action trigger configuration."""

    type: str = Field(..., description="The type of trigger")
    operation: str | SkipJsonSchema[None] = Field(
        None, description="The operation type (CREATE, DAY_2, DELETE)"
    )
    event: str | SkipJsonSchema[None] = Field(
        None, description="The event that triggers the action"
    )
    condition: dict[str, Any] | SkipJsonSchema[None] = Field(
        None, description="Conditions for the trigger"
    )


class ActionInvocationMethod(BaseModel):
    """Action invocation method configuration."""

    type: str = Field(..., description="The type of invocation method")
    url: str | SkipJsonSchema[None] = Field(None, description="URL for webhook invocation")
    agent: bool | SkipJsonSchema[None] = Field(
        None, description="Whether to use agent for invocation"
    )
    method: str | SkipJsonSchema[None] = Field(None, description="HTTP method for webhook")
    headers: dict[str, str] | SkipJsonSchema[None] = Field(None, description="Headers for webhook")
    body: str | dict[str, Any] | SkipJsonSchema[None] = Field(
        None, description="Body template for webhook (can be string or dict)"
    )


class ActionSummary(BaseModel):
    """Simplified Action model with only basic information."""

    identifier: str = Field(..., description="The unique identifier of the action")
    title: str = Field(..., description="The title of the action")
    description: str | SkipJsonSchema[None] = Field(
        None, description="The description of the action"
    )
    blueprint: str | SkipJsonSchema[None] = Field(
        None, description="The blueprint this action belongs to"
    )


class Action(BaseModel):
    """Port.io Action model."""

    identifier: str = Field(..., description="The unique identifier of the action")
    title: str = Field(..., description="The title of the action")
    description: str | SkipJsonSchema[None] = Field(
        None, description="The description of the action"
    )
    icon: Icon | SkipJsonSchema[None] = Field(None, description="The icon of the action")
    blueprint: str | SkipJsonSchema[None] = Field(
        None, description="The blueprint this action belongs to"
    )
    trigger: ActionTrigger = Field(..., description="The trigger configuration")
    invocation_method: ActionInvocationMethod = Field(
        ...,
        description="The invocation method configuration",
        alias="invocationMethod",
        serialization_alias="invocationMethod",
    )
    user_inputs: ActionSchema = Field(
        default_factory=ActionSchema,
        description="User input schema for the action",
        alias="userInputs",
        serialization_alias="userInputs",
    )
    approval_notification: dict[str, Any] | SkipJsonSchema[None] = Field(
        None,
        description="Approval notification configuration",
        alias="approvalNotification",
        serialization_alias="approvalNotification",
    )
    created_at: str | SkipJsonSchema[None] = Field(None, description="Creation timestamp")
    created_by: str | SkipJsonSchema[None] = Field(None, description="Creator user")
    updated_at: str | SkipJsonSchema[None] = Field(None, description="Last update timestamp")
    updated_by: str | SkipJsonSchema[None] = Field(None, description="Last updater user")
