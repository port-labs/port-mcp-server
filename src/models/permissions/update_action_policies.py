"""Update action policies tool schemas."""

from typing import Any

from pydantic import Field

from src.models.common.base_pydantic import BaseModel


class UpdateActionPoliciesToolSchema(BaseModel):
    """Schema for update action policies tool."""
    
    action_identifier: str = Field(
        description="The identifier of the action to update policies for"
    )
    policies: dict[str, Any] = Field(
        description="""Policies configuration to update. This should contain the complete policies structure including:

• **execution**: Defines who can execute the action
  - type: "users", "teams", "roles", "condition" 
  - users/teams/roles: List of allowed users/teams/roles
  - condition: JQ expression for dynamic conditions

• **approval**: Approval workflow configuration
  - required: Boolean indicating if approval is needed
  - approvers: Who can approve (same structure as execution)
  - stages: Multi-stage approval configuration

• **conditions**: Additional dynamic conditions
  - entity_conditions: Conditions based on entity properties
  - user_conditions: Conditions based on user properties

Example structures:
- Team-based: {"execution": {"type": "teams", "teams": ["platform-team"]}}
- Conditional: {"execution": {"type": "condition", "condition": ".entity.properties.owner == .user.email"}}
- With approval: {"execution": {...}, "approval": {"required": true, "approvers": {...}}}"""
    )


class UpdateActionPoliciesToolResponse(BaseModel):
    """Response model for update action policies tool."""
    
    action_identifier: str = Field(description="The action identifier that was updated")
    updated_policies: dict[str, Any] = Field(description="The updated policies configuration")
    success: bool = Field(description="Whether the update was successful")