from pydantic import Field

from .base_pydantic import BaseModel


class Annotations(BaseModel):
    title: str = Field(..., description="A human-readable title for the tool, useful for UI display")
    read_only_hint: bool = Field(
        ...,
        description="If true, indicates the tool does not modify its environment",
        alias="readOnlyHint",
        serialization_alias="readOnlyHint",
    )
    destructive_hint: bool = Field(
        ...,
        description="If true, the tool may perform destructive updates (only meaningful when readOnlyHint is false)",
        alias="destructiveHint",
        serialization_alias="destructiveHint",
    )
    idempotent_hint: bool = Field(
        ...,
        description="If true, calling the tool repeatedly with the same arguments has no additional effect (only meaningful when readOnlyHint is false)",
        alias="idempotentHint",
        serialization_alias="idempotentHint",
    )
    open_world_hint: bool = Field(
        ...,
        description="If true, the tool may interact with an “open world” of external entities",
        alias="openWorldHint",
        serialization_alias="openWorldHint",
    )
