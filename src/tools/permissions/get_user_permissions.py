"""Tool for getting user permissions from Port."""

from typing import Any

from src.client import PortClient
from src.models.common.annotations import Annotations
from src.models.permissions.get_user_permissions import (
    GetUserPermissionsToolResponse,
    GetUserPermissionsToolSchema,
)
from src.models.tools.tool import Tool
from src.utils import logger


class GetUserPermissionsTool(Tool[GetUserPermissionsToolSchema]):
    """Get current user's permissions from Port."""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_user_permissions",
            description="Get the current user's permissions in Port. This includes action execution permissions, entity management permissions, and RBAC-related permissions.",
            input_schema=GetUserPermissionsToolSchema,
            output_schema=GetUserPermissionsToolResponse,
            annotations=Annotations(
                title="Get User Permissions",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.get_user_permissions,
        )
        self.port_client = port_client

    async def get_user_permissions(self, props: GetUserPermissionsToolSchema) -> dict[str, Any]:
        """Get user permissions from Port auth endpoint."""
        logger.info("GetUserPermissionsTool.get_user_permissions called")

        if not self.port_client.permissions:
            raise ValueError("Permissions client not available")

        permissions = await self.port_client.permissions.get_user_permissions()

        response = GetUserPermissionsToolResponse(
            permissions=permissions,
            total_count=len(permissions)
        )
        
        logger.info(f"Retrieved {len(permissions)} user permissions")
        return response.model_dump(exclude_unset=True, exclude_none=True)