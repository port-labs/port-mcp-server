"""Port.io authentication token model."""

from dataclasses import dataclass
from mcp.types import TextContent, GetPromptResult, PromptMessage

@dataclass
class PortToken:
    """Data model for Port authentication token."""
    access_token: str
    expires_in: int
    token_type: str

    def to_text(self) -> str:
        """Convert token to text format."""
        return f"""Authentication successful.
                Token: {self.access_token}
                Expires in: {self.expires_in} seconds
                Token type: {self.token_type}"""

    def to_prompt_result(self) -> GetPromptResult:
        """Convert token to prompt result format."""
        return GetPromptResult(
            description="Port Authentication Token",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=self.to_text())
                )
            ]
        ) 