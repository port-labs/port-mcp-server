"""Tool for getting action permissions configuration."""

from typing import Any

from src.client import PortClient
from src.models.common.annotations import Annotations
from src.models.permissions.get_action_permissions import (
    GetActionPermissionsToolResponse,
    GetActionPermissionsToolSchema,
)
from src.models.tools.tool import Tool
from src.utils import logger


class GetActionPermissionsTool(Tool[GetActionPermissionsToolSchema]):
    """Get permissions and RBAC configuration for a specific action."""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_action_permissions",
            description="Get the permissions, approval, and execution configuration for a specific action in Port. This includes RBAC settings, dynamic permissions, and approval workflows.",
            input_schema=GetActionPermissionsToolSchema,
            output_schema=GetActionPermissionsToolResponse,
            annotations=Annotations(
                title="Get Action Permissions",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.get_action_permissions,
        )
        self.port_client = port_client

    async def get_action_permissions(self, props: GetActionPermissionsToolSchema) -> dict[str, Any]:
        """Get permissions configuration for the specified action."""
        logger.info(f"GetActionPermissionsTool.get_action_permissions called for action: {props.action_identifier}")

        if not self.port_client.permissions:
            raise ValueError("Permissions client not available")

        # Get action permissions configuration
        permissions_info = await self.port_client.permissions.get_action_permissions(
            props.action_identifier
        )
        
        if not permissions_info:
            raise ValueError(f"Action '{props.action_identifier}' not found or no permissions available")

        response = GetActionPermissionsToolResponse(
            permissions=permissions_info
        )
        
        logger.info(f"Retrieved permissions configuration for action '{props.action_identifier}'")
        return response.model_dump(exclude_unset=True, exclude_none=True)