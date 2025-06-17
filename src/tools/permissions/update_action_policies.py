"""Tool for updating action policies."""

from typing import Any

from src.client import PortClient
from src.models.common.annotations import Annotations
from src.models.permissions.update_action_policies import (
    UpdateActionPoliciesToolResponse,
    UpdateActionPoliciesToolSchema,
)
from src.models.tools.tool import Tool
from src.utils import logger


class UpdateActionPoliciesTool(Tool[UpdateActionPoliciesToolSchema]):
    """Update policies configuration for a specific action in Port."""

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_action_policies",
            description="Update policies configuration for a specific action in Port. This allows modifying RBAC settings, approval workflows, and execution policies.",
            input_schema=UpdateActionPoliciesToolSchema,
            output_schema=UpdateActionPoliciesToolResponse,
            annotations=Annotations(
                title="Update Action Policies",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=False,
            ),
            function=self.update_action_policies,
        )
        self.port_client = port_client

    async def update_action_policies(self, props: UpdateActionPoliciesToolSchema) -> dict[str, Any]:
        """Update policies configuration for the specified action."""
        logger.info(f"UpdateActionPoliciesTool.update_action_policies called for action: {props.action_identifier}")

        if not self.port_client.permissions:
            raise ValueError("Permissions client not available")

        # Update action policies using the permissions client
        result = await self.port_client.permissions.update_action_policies(
            props.action_identifier, props.policies
        )

        response = UpdateActionPoliciesToolResponse(
            action_identifier=result.get("action_identifier", props.action_identifier),
            updated_policies=result.get("updated_policies", {}),
            success=result.get("success", False)
        )
        
        logger.info(f"Policy update result for '{props.action_identifier}': {response.success}")
        return response.model_dump(exclude_unset=True, exclude_none=True)