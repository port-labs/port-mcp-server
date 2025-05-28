from typing import Any, Self

from pydantic import Field, ModelWrapValidatorHandler, ValidationError, model_validator
from pydantic.json_schema import SkipJsonSchema

from src.models.common.base_pydantic import BaseModel
from src.models.scorecards.schemas import ScorecardLevelSchema, ScorecardRuleSchema, ScorecardRuleSchemaExplicitForTool


class ScorecardCommon(BaseModel):
    identifier: str = Field(..., description="The identifier of the scorecard to create")
    title: str = Field(..., description="The title of the scorecard to create")
    levels: list[ScorecardLevelSchema] | SkipJsonSchema[None] = Field(
        None,
        description="Levels are the different stages that an entity can be in, according to the rules that it passes.",
    )
    rules: list[ScorecardRuleSchema] = Field(
        ...,
        description="Rules enable you to generate checks inside a scorecard only for entities and properties. Rules are not allowed to reference the first level defined in the levels array(MUST).",
    )


class ScorecardCommonExplicitForTool(BaseModel):
    identifier: str = Field(..., description="The identifier of the scorecard to create")
    title: str = Field(..., description="The title of the scorecard to create")
    levels: list[ScorecardLevelSchema] | SkipJsonSchema[None] = Field(
        None,
        description="Levels are the different stages that an entity can be in, according to the rules that it passes.",
    )
    rules: list[ScorecardRuleSchemaExplicitForTool] = Field(
        ...,
        description="Rules enable you to generate checks inside a scorecard only for entities and properties. Rules are not allowed to reference the first level defined in the levels array(MUST).",
    )


class Scorecard(ScorecardCommon):
    blueprint: str = Field(..., description="The blueprint of the scorecard")
    id: str = Field(..., description="The id of the scorecard")
    created_at: str | SkipJsonSchema[None] = Field(None, description="The created at date of the scorecard")
    created_by: str | SkipJsonSchema[None] = Field(None, description="The created by user of the scorecard")
    updated_at: str | SkipJsonSchema[None] = Field(None, description="The updated at date of the scorecard")
    updated_by: str | SkipJsonSchema[None] = Field(None, description="The updated by user of the scorecard")


class ScorecardCreate(ScorecardCommonExplicitForTool):
    @model_validator(mode="wrap")
    @classmethod
    def log_failed_validation(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        try:
            return handler(data)
        except ValidationError as e:
            for error in e.errors():
                if error["type"] == "missing" and "condition_name" in error["loc"]:
                    raise ValueError(
                        "condition_name is required within rules[index].query.conditions[index].condition_name"
                    ) from e
            raise e


class ScorecardUpdate(ScorecardCommonExplicitForTool):
    pass
