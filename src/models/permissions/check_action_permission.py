"""Check action permission tool schemas."""

from pydantic import Field

from src.models.common.base_pydantic import BaseModel


class CheckActionPermissionToolSchema(BaseModel):
    """Schema for check action permission tool."""
    
    action_identifier: str = Field(description="The identifier of the action to check permissions for")


class CheckActionPermissionToolResponse(BaseModel):
    """Response model for check action permission tool."""
    
    action_identifier: str = Field(description="The action identifier that was checked")
    has_permission: bool = Field(description="Whether the user has permission to execute this action")
    permission_types: list[str] = Field(description="List of relevant permission types found")