"""Update action policies tool schemas."""

from typing import Any

from pydantic import Field

from src.models.common.base_pydantic import BaseModel


class UpdateActionPoliciesToolSchema(BaseModel):
    """Schema for update action policies tool."""
    
    action_identifier: str = Field(description="The identifier of the action to update policies for")
    policies: dict[str, Any] = Field(description="Policies configuration to update")


class UpdateActionPoliciesToolResponse(BaseModel):
    """Response model for update action policies tool."""
    
    action_identifier: str = Field(description="The action identifier that was updated")
    updated_policies: dict[str, Any] = Field(description="The updated policies configuration")
    success: bool = Field(description="Whether the update was successful")