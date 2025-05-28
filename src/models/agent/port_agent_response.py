"""Port.io AI agent response model."""

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.models.common.base_pydantic import BaseModel


class PortAgentInvocation(BaseModel):
    identifier: str = Field(..., description="The identifier of the invocation")


class PortAgentTriggerResponse(BaseModel):
    ok: bool = Field(..., description="Whether the request was successful")
    invocation: PortAgentInvocation = Field(..., description="The invocation data")


class PortAgentResponse(BaseModel):
    identifier: str = Field(..., description="The identifier of the agent response")
    status: str = Field(..., description="The status of the agent response")
    raw_output: str | SkipJsonSchema[None] = Field(None, description="The raw output of the agent response")
    output: str | SkipJsonSchema[None] = Field(None, description="The output of the agent response")
    error: str | SkipJsonSchema[None] = Field(None, description="The error of the agent response")
    action_url: str | SkipJsonSchema[None] = Field(None, description="The action URL of requied to visit to complete the action")
    selected_agent: str | SkipJsonSchema[None] = Field(None, description="The selected agent that generated the response")
