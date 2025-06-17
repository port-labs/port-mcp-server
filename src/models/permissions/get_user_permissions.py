"""Get user permissions tool schemas."""

from pydantic import Field

from src.models.common.base_pydantic import BaseModel


class GetUserPermissionsToolSchema(BaseModel):
    """Schema for get user permissions tool - no input parameters needed."""
    pass


class GetUserPermissionsToolResponse(BaseModel):
    """Response model for get user permissions tool."""
    
    permissions: list[str] = Field(description="List of user permissions")
    total_count: int = Field(description="Total number of permissions")