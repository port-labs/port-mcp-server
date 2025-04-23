"""Port.io scorecard model."""

from typing import List, Optional
from src.server.models.scorecards.schemas import ScorecardLevelSchema, ScorecardRuleSchema
from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
class ScorecardCommon(BaseModel):
    identifier: str = Field(..., description="The identifier of the scorecard to create")
    title: str = Field(..., description="The title of the scorecard to create")
    levels: List[ScorecardLevelSchema] | SkipJsonSchema[None] = Field(None, description="Levels are the different stages that an entity can be in, according to the rules that it passes.")
    rules: List[ScorecardRuleSchema] = Field(..., description="Rules enable you to generate checks inside a scorecard only for entities and properties. Rules are not allowed to reference the first level defined in the levels array(MUST).")
class Scorecard(ScorecardCommon):
    """Data model for Port scorecard."""
    blueprint: str = Field(..., description="The blueprint of the scorecard")
    id: str = Field(..., description="The id of the scorecard")
    created_at: str | SkipJsonSchema[None] = Field(None, description="The created at date of the scorecard")
    created_by: str | SkipJsonSchema[None] = Field(None, description="The created by user of the scorecard")
    updated_at: str | SkipJsonSchema[None] = Field(None, description="The updated at date of the scorecard")
    updated_by: str | SkipJsonSchema[None] = Field(None, description="The updated by user of the scorecard")
class ScorecardCreate(ScorecardCommon):
    pass