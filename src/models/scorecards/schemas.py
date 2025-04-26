from typing import Literal

from pydantic import Field

from src.models.common.base_pydantic import BaseModel

from .condition_property import (
    ScorecardConditionPropertyBetweenConditionSchema,
    ScorecardConditionPropertyComparisonConditionSchema,
    ScorecardConditionPropertyContainsAnyConditionSchema,
    ScorecardConditionPropertyEmptyConditionSchema,
    ScorecardConditionRelationComparisonConditionSchema,
    ScorecardConditionRelationEmptyConditionSchema,
)
from .condition_property_tool import (
    ScorecardConditionPropertyBetweenConditionSchemaExplicitForTool,
    ScorecardConditionPropertyComparisonConditionSchemaExplicitForTool,
    ScorecardConditionPropertyContainsAnyConditionSchemaExplicitForTool,
    ScorecardConditionPropertyEmptyConditionSchemaExplicitForTool,
    ScorecardConditionRelationComparisonConditionSchemaExplicitForTool,
    ScorecardConditionRelationEmptyConditionSchemaExplicitForTool,
)


class ScorecardLevelSchema(BaseModel):
    title: str = Field(..., description="The title of the level to create")
    color: Literal[
        "blue",
        "turquoise",
        "orange",
        "purple",
        "pink",
        "yellow",
        "green",
        "red",
        "gold",
        "silver",
        "paleBlue",
        "darkGray",
        "lightGray",
        "bronze",
    ] = Field(..., description="The color of the level to create")


class ScorecardQuerySchema(BaseModel):
    combinator: Literal["and", "or"] = Field(..., description="The combinator of the rule to create")
    conditions: list[
        ScorecardConditionPropertyBetweenConditionSchema
        | ScorecardConditionPropertyContainsAnyConditionSchema
        | ScorecardConditionPropertyEmptyConditionSchema
        | ScorecardConditionRelationEmptyConditionSchema
        | ScorecardConditionRelationComparisonConditionSchema
        | ScorecardConditionPropertyComparisonConditionSchema
    ] = Field(
        ...,
        description="Pay extreme attention to the conditions schema and the required fields, they are small boolean checks that help when determining the final status of a query according to the specified combinator",
    )


class ScorecardQuerySchemaExplicitForTool(BaseModel):
    combinator: Literal["and", "or"] = Field(..., description="The combinator of the rule to create")
    conditions: list[
        ScorecardConditionPropertyBetweenConditionSchemaExplicitForTool
        | ScorecardConditionPropertyContainsAnyConditionSchemaExplicitForTool
        | ScorecardConditionPropertyEmptyConditionSchemaExplicitForTool
        | ScorecardConditionRelationEmptyConditionSchemaExplicitForTool
        | ScorecardConditionRelationComparisonConditionSchemaExplicitForTool
        | ScorecardConditionPropertyComparisonConditionSchemaExplicitForTool
    ] = Field(
        ...,
        description="Pay extreme attention to the conditions schema and the required fields, they are small boolean checks that help when determining the final status of a query according to the specified combinator",
    )


class ScorecardRuleSchema(BaseModel):
    identifier: str = Field(
        ...,
        pattern=r"^[A-Za-z0-9@_.:\\/=-]+$",
        max_length=20,
        description="The identifier of the rule to create",
    )
    title: str = Field(..., description="The title of the rule to create")
    level: str = Field(
        ...,
        description="The level of the rule to create, must be a valid level - cant be the first level in the scorecard",
    )
    query: ScorecardQuerySchema = Field(..., description="The query of the rule to create")
    description: str = Field(..., description="The description of the rule to create")


class ScorecardRuleSchemaExplicitForTool(BaseModel):
    identifier: str = Field(
        ...,
        pattern=r"^[A-Za-z0-9@_.:\\/=-]+$",
        max_length=20,
        description="The identifier of the rule to create",
    )
    title: str = Field(..., description="The title of the rule to create")
    level: str = Field(..., description="The level of the rule to create")
    query: ScorecardQuerySchemaExplicitForTool = Field(..., description="The query of the rule to create")
    description: str = Field(..., description="The description of the rule to create")
