from dataclasses import dataclass
from typing import Optional
from mcp.types import TextContent, GetPromptResult, PromptMessage

@dataclass
class PortToken:
    """Data model for Port.io authentication token."""
    access_token: str
    expires_in: int
    token_type: str

    def to_text(self) -> str:
        return f"""Authentication successful.
                Token: {self.access_token}
                Expires in: {self.expires_in} seconds
                Token type: {self.token_type}"""

    def to_prompt_result(self) -> GetPromptResult:
        return GetPromptResult(
            description="Port Authentication Token",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=self.to_text())
                )
            ]
        )

@dataclass
class PortBlueprint:
    """Data model for Port.io blueprint."""
    title: str
    identifier: str
    description: Optional[str] = None

    def to_text(self) -> str:
        desc = f"\nDescription: {self.description}" if self.description else ""
        return f"{self.title} (ID: {self.identifier}){desc}"

@dataclass
class PortAgentResponse:
    """Data model for Port.io AI agent response."""
    identifier: str
    status: str
    raw_output: Optional[str] = None
    output: Optional[str] = None
    error: Optional[str] = None
    action_url: Optional[str] = None

    def to_text(self) -> str:
        if self.error:
            return f"❌ Error: {self.error}"
        
        if self.status.lower() == "completed":
            response_text = f"✅ Completed!\n\nResponse:\n{self.output}"
            
            # If there's an action URL, add clear instructions
            if self.action_url:
                response_text += f"\n\n🔍 Action Required:\n"
                response_text += f"To complete this action, please visit:\n{self.action_url}"
            return response_text
            
        return f"Status: {self.status}\nIdentifier: {self.identifier}"
