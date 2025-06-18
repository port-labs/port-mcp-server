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
    """Update policies configuration for a specific action in Port.
    
    This tool enables updating Port's dynamic permissions and RBAC policies for actions.
    Port's dynamic permissions system allows flexible permission assignment based on:
    
    - User properties (e.g., team membership, role)
    - Entity properties (e.g., entity ownership, blueprint, properties)
    - Time-based conditions
    - Custom policies using JQ expressions
    
    The policies configuration includes:
    - Execution permissions: Who can execute the action
    - Approval workflows: Multi-stage approval requirements
    - Conditions: Dynamic conditions for permission evaluation
    - Teams and roles: Team-based and role-based access control
    
    Example policy configurations:
    - Team-based: Allow only specific teams to execute actions
    - Entity ownership: Allow only entity owners to perform actions
    - Conditional: Apply different permissions based on entity properties
    - Approval workflows: Require approvals before action execution
    """

    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_action_policies",
            description="""Update policies configuration for a specific action in Port's dynamic permissions system. 

This tool allows comprehensive configuration of RBAC policies and permissions for actions, including:

• **Execution Permissions**: Define who can execute the action using user properties, teams, roles, or custom conditions
• **Approval Workflows**: Configure multi-stage approval processes with different approval requirements
• **Dynamic Conditions**: Set up conditional permissions based on entity properties, user attributes, or custom JQ expressions
• **Team-based Access**: Restrict access to specific teams or team members
• **Entity-based Permissions**: Apply permissions based on entity ownership, blueprint, or properties

**🔑 CRITICAL LEARNINGS & BEST PRACTICES:**

**1. Team Membership Queries:**
- ✅ **CORRECT**: Use `"property": "$team"` (meta property) for querying user team membership
- ❌ **INCORRECT**: Using `"property": "team"` (regular property) will not work
- Use `"operator": "containsAny"` with team arrays: `["aws-experts", "platform-team"]`

**2. Approval Conditions - Return User Identifiers:**
- ✅ **CORRECT**: Approval conditions MUST return arrays of user identifiers
- ❌ **INCORRECT**: Don't return boolean values or check `length > 0`
- Example: `[.results.experts.entities[].identifier]` ✅
- Not: `[.results.experts.entities[].identifier] | length > 0` ❌

**3. Query Structure for User Team Membership:**
```json
{
  "rules": [
    {"property": "$blueprint", "operator": "=", "value": "_user"},
    {"property": "$team", "operator": "containsAny", "value": ["team-name"]}
  ],
  "combinator": "and"
}
```

**Policy Structure Examples:**

1. **Team-based permissions**:
   ```json
   {
     "execute": {
       "roles": ["Member"],
       "teams": ["platform-team", "dev-ops"]
     }
   }
   ```

2. **Cloud Provider Expertise-based Approval (Advanced)**:
   ```json
   {
     "execute": {"roles": ["Member"]},
     "approve": {
       "roles": ["Admin"],
       "policy": {
         "queries": {
           "awsExperts": {
             "rules": [
               {"property": "$blueprint", "operator": "=", "value": "_user"},
               {"property": "$team", "operator": "containsAny", "value": ["aws-experts"]}
             ],
             "combinator": "and"
           }
         },
         "conditions": [
           "if .inputs.cloud_provider == \\"AWS\\" then [.results.awsExperts.entities[].identifier] else [] end"
         ]
       }
     }
   }
   ```

3. **Prevent Self-Approval**:
   ```json
   {
     "execute": {"roles": ["Member"]},
     "approve": {
       "policy": {
         "queries": {
           "allApprovers": {
             "rules": [{"property": "$blueprint", "operator": "=", "value": "_user"}],
             "combinator": "and"
           }
         },
         "conditions": [
           "[.results.allApprovers.entities[] | select(.identifier != \\"{{.trigger.user.email}}\\") | .identifier]"
         ]
       }
     }
   }
   ```

Supports Port's full dynamic permissions capabilities as described in the Port documentation.""",
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