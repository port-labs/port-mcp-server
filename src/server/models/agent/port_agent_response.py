"""Port.io AI agent response model."""

from dataclasses import Field, dataclass
from typing import Optional

from src.server.models import BaseModel

class PortAgentResponse(BaseModel):
    identifier: str = Field(..., description="The identifier of the agent response")
    status: str = Field(..., description="The status of the agent response")
    raw_output: Optional[str] = Field(None, description="The raw output of the agent response")
    output: Optional[str] = Field(None, description="The output of the agent response")
    error: Optional[str] = Field(None, description="The error of the agent response")
    action_url: Optional[str] = Field(None, description="The action URL of requied to visit to complete the action")
