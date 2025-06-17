"""Tool for checking action permissions."""

from typing import Any

from src.client import PortClient
from src.models.common.annotations import Annotations
from src.models.permissions.check_action_permission import (
    CheckActionPermissionToolResponse,
    CheckActionPermissionToolSchema,
)
from src.models.tools.tool import Tool
from src.utils import logger


class CheckActionPermissionTool(Tool[CheckActionPermissionToolSchema]):
    """Check if the current user has permission to execute a specific action."""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="check_action_permission",
            description="Check if the current user has permission to execute a specific action in Port. This validates both direct action permissions and team-based permissions.",
            input_schema=CheckActionPermissionToolSchema,
            output_schema=CheckActionPermissionToolResponse,
            annotations=Annotations(
                title="Check Action Permission",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.check_action_permission,
        )
        self.port_client = port_client

    async def check_action_permission(self, props: CheckActionPermissionToolSchema) -> dict[str, Any]:
        """Check if user has permission to execute the specified action."""
        logger.info(f"CheckActionPermissionTool.check_action_permission called for action: {props.action_identifier}")

        if not self.port_client.permissions:
            raise ValueError("Permissions client not available")

        # Get user permissions
        permissions = await self.port_client.permissions.get_user_permissions()
        
        # Check permission using the permissions client
        has_permission = self.port_client.permissions.check_action_permission(
            props.action_identifier, permissions
        )
        
        # Determine which permission types are relevant
        execute_action_permission = f"execute:actions:{props.action_identifier}"
        team_execute_permission = f"execute:team_entities:actions:{props.action_identifier}"
        
        permission_types = []
        if execute_action_permission in permissions:
            permission_types.append("execute:actions")
        if team_execute_permission in permissions:
            permission_types.append("execute:team_entities:actions")

        response = CheckActionPermissionToolResponse(
            action_identifier=props.action_identifier,
            has_permission=has_permission,
            permission_types=permission_types
        )
        
        logger.info(f"Permission check result for '{props.action_identifier}': {has_permission}")
        return response.model_dump(exclude_unset=True, exclude_none=True)