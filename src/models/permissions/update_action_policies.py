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

• **execute**: Execution permissions configuration
  - roles: List of roles allowed to execute (e.g., ["Member", "Admin"])
  - users: List of specific users allowed to execute
  - teams: List of teams allowed to execute  
  - ownedByTeam: Boolean indicating if team ownership is required
  - policy: Dynamic policy with queries and conditions

• **approve**: Approval workflow configuration
  - roles: List of roles allowed to approve
  - users: List of specific users allowed to approve
  - teams: List of teams allowed to approve
  - policy: Dynamic policy with queries and conditions for approval

• **policy**: Dynamic conditions using queries and JQ expressions
  - queries: Named queries to fetch entities/users
  - conditions: JQ expressions that evaluate to true/false

🔑 **CRITICAL IMPLEMENTATION NOTES:**

1. **Team Queries**: Use "$team" meta property, not "team" regular property
   - Correct: {"property": "$team", "operator": "containsAny", "value": ["team-name"]}
   - Wrong: {"property": "team", "operator": "containsAny", "value": ["team-name"]}

2. **Approval Conditions**: MUST return user identifier arrays, not booleans
   - Correct: [.results.experts.entities[].identifier]
   - Wrong: [.results.experts.entities[].identifier] | length > 0

3. **User Team Membership Query Pattern**:
   ```json
   {
     "rules": [
       {"property": "$blueprint", "operator": "=", "value": "_user"},
       {"property": "$team", "operator": "containsAny", "value": ["team-name"]}
     ],
     "combinator": "and"
   }
   ```

Example structures based on Port's dynamic permissions:
- Basic team-based: {"execute": {"roles": ["Member"], "teams": ["platform-team"]}}
- Dynamic condition: {"execute": {"roles": ["Member"], "policy": {"queries": {...}, "conditions": [...]}}}
- With approval workflow: {"execute": {...}, "approve": {"roles": ["Admin"], "policy": {...}}}
- Prevent self-approval: Use policy conditions to exclude the executing user from approvers

Supports Port's full dynamic permissions capabilities as described in the Port documentation."""
    )



class UpdateActionPoliciesToolResponse(BaseModel):
    """Response model for update action policies tool."""
    
    action_identifier: str = Field(description="The action identifier that was updated")
    updated_policies: dict[str, Any] = Field(description="The updated policies configuration")
    success: bool = Field(description="Whether the update was successful")