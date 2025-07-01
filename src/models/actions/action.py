"""Port.io action model."""

from typing import Any, Literal

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
        None, description="The operation type (CREATE, DAY-2, DELETE)"
    )
    event: str | SkipJsonSchema[None] = Field(
        None, description="The event that triggers the action"
    )
    condition: dict[str, Any] | SkipJsonSchema[None] = Field(
        None, description="Conditions for the trigger"
    )
    user_inputs: ActionSchema | SkipJsonSchema[None] = Field(
        None, description="User input schema for the trigger", alias="userInputs"
    )
    blueprint_identifier: str | SkipJsonSchema[None] = Field(
        None, description="The blueprint identifier for the trigger", alias="blueprintIdentifier"
    )


class ActionInvocationMethodGitHub(BaseModel):
    """GitHub invocation method configuration."""

    type: Literal["GITHUB"] = Field(..., description="The type of invocation method")
    org: str = Field(..., description="GitHub organization")
    repo: str = Field(..., description="GitHub repository")
    workflow: str = Field(..., description="GitHub workflow filename")
    omit_payload: bool | SkipJsonSchema[None] = Field(None, description="Whether to omit payload")
    omit_user_inputs: bool | SkipJsonSchema[None] = Field(
        None, description="Whether to omit user inputs"
    )
    report_workflow_status: bool | SkipJsonSchema[None] = Field(
        None, description="Whether to report workflow status"
    )


class ActionInvocationMethodGitLab(BaseModel):
    """GitLab invocation method configuration."""

    type: Literal["GITLAB"] = Field(..., description="The type of invocation method")
    project_name: str = Field(..., description="GitLab project name", alias="projectName")
    group_name: str = Field(..., description="GitLab group name", alias="groupName")
    agent: Literal[True] = Field(..., description="Agent must be true for GitLab")
    omit_payload: bool | SkipJsonSchema[None] = Field(
        None, description="Whether to omit payload", alias="omitPayload"
    )
    omit_user_inputs: bool | SkipJsonSchema[None] = Field(
        None, description="Whether to omit user inputs", alias="omitUserInputs"
    )
    default_ref: str | SkipJsonSchema[None] = Field(
        None, description="Default Git reference", alias="defaultRef"
    )


class ActionInvocationMethodAzureDevOps(BaseModel):
    """Azure DevOps invocation method configuration."""

    type: Literal["AZURE-DEVOPS"] = Field(..., description="The type of invocation method")
    org: str = Field(..., description="Azure DevOps organization")
    webhook: str = Field(..., description="Azure DevOps webhook URL")


class ActionInvocationMethodWebhook(BaseModel):
    """Webhook invocation method configuration."""

    type: Literal["WEBHOOK"] = Field(..., description="The type of invocation method")
    url: str = Field(..., description="Webhook URL")
    agent: bool | SkipJsonSchema[None] = Field(
        None, description="Whether to use agent for invocation"
    )
    synchronized: bool | SkipJsonSchema[None] = Field(
        None, description="Whether the webhook is synchronized"
    )
    method: Literal["POST", "DELETE", "PATCH", "PUT"] | SkipJsonSchema[None] = Field(
        None, description="HTTP method for webhook"
    )
    headers: dict[str, str] | SkipJsonSchema[None] = Field(None, description="Headers for webhook")
    body: str | dict[str, Any] | SkipJsonSchema[None] = Field(
        None, description="Body template for webhook (can be string or dict)"
    )


class ActionInvocationMethodKafka(BaseModel):
    """Kafka invocation method configuration."""

    type: Literal["KAFKA"] = Field(..., description="The type of invocation method")


# Union type for all invocation methods
ActionInvocationMethod = (
    ActionInvocationMethodGitHub
    | ActionInvocationMethodGitLab
    | ActionInvocationMethodAzureDevOps
    | ActionInvocationMethodWebhook
    | ActionInvocationMethodKafka
)


class ActionCommon(BaseModel):
    """Common fields for action models."""

    identifier: str = Field(..., description="The unique identifier of the action")
    title: str = Field(..., description="The title of the action")
    description: str | SkipJsonSchema[None] = Field(
        None, description="The description of the action"
    )
    icon: Icon | SkipJsonSchema[None] = Field(None, description="The icon of the action")
    trigger: ActionTrigger = Field(..., description="The trigger configuration")
    invocation_method: ActionInvocationMethod = Field(
        ...,
        description="The invocation method configuration. Must be a JSON object (not a string) with 'type' field and method-specific properties.",
        alias="invocationMethod",
        serialization_alias="invocationMethod",
    )
    required_approval: bool | SkipJsonSchema[None] = Field(
        None,
        description="Whether approval is required",
        alias="requiredApproval",
        serialization_alias="requiredApproval",
    )
    approval_notification: dict[str, Any] | SkipJsonSchema[None] = Field(
        None,
        description="Approval notification configuration",
        alias="approvalNotification",
        serialization_alias="approvalNotification",
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


class Action(ActionCommon):
    """Port.io Action model."""

    created_at: str | SkipJsonSchema[None] = Field(None, description="Creation timestamp")
    created_by: str | SkipJsonSchema[None] = Field(None, description="Creator user")
    updated_at: str | SkipJsonSchema[None] = Field(None, description="Last update timestamp")
    updated_by: str | SkipJsonSchema[None] = Field(None, description="Last updater user")


class ActionCreate(ActionCommon):
    """Model for creating a new action."""

    pass


class ActionUpdate(ActionCommon):
    """Model for updating an existing action."""

    pass
