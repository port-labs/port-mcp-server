from pydantic import Field
from .base_pydantic import BaseModel


class Annotations(BaseModel):
    title: str = Field(..., description="A human-readable title for the tool, useful for UI display")
    readOnlyHint: bool = Field(..., description="If true, indicates the tool does not modify its environment")
    destructiveHint: bool = Field(..., description="If true, the tool may perform destructive updates (only meaningful when readOnlyHint is false)")
    idempotentHint: bool = Field(..., description="If true, calling the tool repeatedly with the same arguments has no additional effect (only meaningful when readOnlyHint is false)")
    openWorldHint: bool = Field(..., description="If true, the tool may interact with an “open world” of external entities")
