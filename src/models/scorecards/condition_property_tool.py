from typing import Literal

from pydantic import Field

from .condition_property import (
    ScorecardConditionPropertyBetweenConditionSchema,
    ScorecardConditionPropertyComparisonConditionSchema,
    ScorecardConditionPropertyContainsAnyConditionSchema,
    ScorecardConditionPropertyEmptyConditionSchema,
    ScorecardConditionRelationComparisonConditionSchema,
    ScorecardConditionRelationEmptyConditionSchema,
)


class ScorecardConditionPropertyBetweenConditionSchemaExplicitForTool(ScorecardConditionPropertyBetweenConditionSchema):
    condition_name: Literal["propertyBetween"] = Field(
        ..., exclude=True, description="Must be set to identify the condition type and use it"
    )


class ScorecardConditionPropertyContainsAnyConditionSchemaExplicitForTool(ScorecardConditionPropertyContainsAnyConditionSchema):
    condition_name: Literal["propertyContainsAny"] = Field(
        ..., exclude=True, description="Must be set to identify the condition type and use it"
    )


class ScorecardConditionRelationComparisonConditionSchemaExplicitForTool(ScorecardConditionRelationComparisonConditionSchema):
    condition_name: Literal["relationComparison"] = Field(
        ..., exclude=True, description="Must be set to identify the condition type and use it"
    )


class ScorecardConditionPropertyComparisonConditionSchemaExplicitForTool(ScorecardConditionPropertyComparisonConditionSchema):
    condition_name: Literal["propertyComparison"] = Field(
        ..., exclude=True, description="Must be set to identify the condition type and use it"
    )


class ScorecardConditionPropertyEmptyConditionSchemaExplicitForTool(ScorecardConditionPropertyEmptyConditionSchema):
    condition_name: Literal["propertyEmpty"] = Field(
        ..., exclude=True, description="Must be set to identify the condition type and use it"
    )


class ScorecardConditionRelationEmptyConditionSchemaExplicitForTool(ScorecardConditionRelationEmptyConditionSchema):
    condition_name: Literal["relationEmpty"] = Field(
        ..., exclude=True, description="Must be set to identify the condition type and use it"
    )
