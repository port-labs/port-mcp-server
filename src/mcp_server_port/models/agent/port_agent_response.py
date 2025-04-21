"""Port.io AI agent response model."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class PortAgentResponse:
    """Data model for Port AI agent response."""
    identifier: str
    status: str
    raw_output: Optional[str] = None
    output: Optional[str] = None
    error: Optional[str] = None
    action_url: Optional[str] = None

    def to_text(self) -> str:
        """Convert agent response to text format."""
        if self.error:
            return f"❌ Error: {self.error}"
        
        if self.status.lower() == "completed":
            response_text = f"✅ Completed!\n\nResponse:\n{self.output}"
            
            # If there's an action URL, add clear instructions
            if self.action_url:
                response_text += "\n\n🔍 Action Required:\n"
                response_text += f"To complete this action, please visit:\n{self.action_url}"
            return response_text
            
        return f"Status: {self.status}\nIdentifier: {self.identifier}" 