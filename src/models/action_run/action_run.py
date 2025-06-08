"""Port.io action model."""

from typing import Any

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.models.common.base_pydantic import BaseModel


class ActionRunReference(BaseModel):
    """Reference to a blueprint, entity, or action in an action run."""

    identifier: str = Field(..., description="The identifier of the referenced item")
    title: str = Field(..., description="The title of the referenced item")
    icon: str | SkipJsonSchema[None] = Field(None, description="The icon of the referenced item")
    deleted: bool | SkipJsonSchema[None] = Field(None, description="Whether the referenced item is deleted")


class ActionRunApproval(BaseModel):
    """Approval information for an action run."""

    description: str | SkipJsonSchema[None] = Field(None, description="Approval description")
    user_id: str | SkipJsonSchema[None] = Field(None, description="User ID who approved", alias="userId")
    state: str | SkipJsonSchema[None] = Field(None, description="Approval state")


class ActionRunRequiredApproval(BaseModel):
    """Required approval configuration for an action run."""

    type: str = Field(..., description="Type of approval required")


class ActionRunPayload(BaseModel):
    """Payload configuration for an action run."""

    type: str | SkipJsonSchema[None] = Field(None, description="Payload type")
    url: str | SkipJsonSchema[None] = Field(None, description="Webhook URL")
    agent: bool | SkipJsonSchema[None] = Field(None, description="Whether to use agent")
    synchronized: bool | SkipJsonSchema[None] = Field(None, description="Whether execution is synchronized")
    method: str | SkipJsonSchema[None] = Field(None, description="HTTP method")
    headers: dict[str, str] | SkipJsonSchema[None] = Field(None, description="HTTP headers")
    body: dict[str, Any] | SkipJsonSchema[None] = Field(None, description="Request body")


class ActionRun(BaseModel):
    """Port.io Action Run model representing an execution of an action."""

    id: str = Field(..., description="The unique identifier of the action run")
    blueprint: ActionRunReference | SkipJsonSchema[None] = Field(None, description="Reference to the blueprint")
    entity: ActionRunReference | SkipJsonSchema[None] = Field(None, description="Reference to the entity")
    action: ActionRunReference = Field(..., description="Reference to the action")
    properties: dict[str, Any] = Field(default_factory=dict, description="Input properties provided for this run")
    ended_at: str | SkipJsonSchema[None] = Field(None, description="When the run ended", alias="endedAt")
    source: dict[str, Any] | SkipJsonSchema[None] = Field(None, description="Source information for the run")
    required_approval: ActionRunRequiredApproval | SkipJsonSchema[None] = Field(
        None, description="Required approval configuration", alias="requiredApproval"
    )
    status: str = Field(..., description="The current status of the action run")
    status_label: str | SkipJsonSchema[None] = Field(None, description="Human-readable status label", alias="statusLabel")
    link: list[str] | SkipJsonSchema[None] = Field(None, description="Links related to the run")
    summary: str | SkipJsonSchema[None] = Field(None, description="Run summary")
    approval: ActionRunApproval | SkipJsonSchema[None] = Field(None, description="Approval information")
    payload: ActionRunPayload | SkipJsonSchema[None] = Field(None, description="Payload configuration")
    response: list[str] | SkipJsonSchema[None] = Field(None, description="Response from the action execution")
    created_by: str | SkipJsonSchema[None] = Field(None, description="User who created the run", alias="createdBy")
    updated_by: str | SkipJsonSchema[None] = Field(None, description="User who last updated the run", alias="updatedBy")
    created_at: str | SkipJsonSchema[None] = Field(None, description="Creation timestamp", alias="createdAt")
    updated_at: str | SkipJsonSchema[None] = Field(None, description="Last update timestamp", alias="updatedAt")


class ActionRunsResponse(BaseModel):
    """Response model for listing action runs."""

    ok: bool = Field(..., description="Whether the request was successful")
    runs: list[ActionRun] = Field(..., description="List of action runs")
