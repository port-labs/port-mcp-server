"""Get action permissions tool schemas."""

from typing import Any

from pydantic import Field

from src.models.common.base_pydantic import BaseModel


class GetActionPermissionsToolSchema(BaseModel):
    """Schema for get action permissions tool."""
    
    action_identifier: str = Field(description="The identifier of the action to get permissions configuration for")


class GetActionPermissionsToolResponse(BaseModel):
    """Response model for get action permissions tool."""
    
    permissions: dict[str, Any] = Field(description="Permissions configuration for the action")