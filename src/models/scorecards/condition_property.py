import datetime
from typing import Literal

from pydantic import Field

from src.models.common.base_pydantic import BaseModel


class DateRangeSchema(BaseModel):
    from_date: datetime.datetime = Field(..., description="The start date of the range", alias="from", serialization_alias="from")
    to_date: datetime.datetime = Field(..., description="The end date of the range", alias="to", serialization_alias="to")


class DatePresetSchema(BaseModel):
    preset: Literal[
        "today",
        "tomorrow",
        "yesterday",
        "lastWeek",
        "last2Weeks",
        "lastMonth",
        "last3Months",
        "last6Months",
        "last12Months",
    ] = Field(..., description="Presets of date ranges")


class ScorecardConditionPropertyBetweenConditionSchema(BaseModel):
    property: str = Field(..., description="A date property defined in the blueprint")
    operator: Literal["between", "notBetween", "="] = Field(..., description="Operator to use when evaluating this rule")
    value: DateRangeSchema | DatePresetSchema = Field(..., description="Date value to compare to")


class ScorecardConditionPropertyContainsAnyConditionSchema(BaseModel):
    property: str = Field(..., description="A property defined in the blueprint")
    operator: Literal["containsAny"] = Field(
        ..., description="Operator eveluates if the property contains any of the values in the list"
    )
    value: list[str] = Field(..., description="List of values to compare to")


class ScorecardConditionRelationComparisonConditionSchema(BaseModel):
    relation: str = Field(..., description="A relation defined in the blueprint")
    operator: Literal[
        "=",
        "!=",
        "contains",
        "doesNotContains",
        "beginsWith",
        "doesNotBeginsWith",
        "endsWith",
        "doesNotEndsWith",
    ] = Field(..., description="Operator to use when evaluating this rule")
    value: str | int | float | bool = Field(..., description="Value to compare to")


class ScorecardConditionPropertyComparisonConditionSchema(BaseModel):
    property: str = Field(..., description="A property defined in the blueprint")
    operator: Literal[
        "=",
        "!=",
        ">",
        "<",
        ">=",
        "<=",
        "contains",
        "doesNotContains",
        "beginsWith",
        "doesNotBeginsWith",
        "endsWith",
        "doesNotEndsWith",
    ] = Field(..., description="Operator to use when evaluating this rule")
    value: str | int | bool = Field(..., description="Value to compare to")


class ScorecardConditionPropertyEmptyConditionSchema(BaseModel):
    property: str = Field(..., description="A property defined in the blueprint")
    operator: Literal["isEmpty", "isNotEmpty"] = Field(..., description="Operator to use when evaluating this rule")
    not_: bool = Field(False, description="Negate the result of the rule")


class ScorecardConditionRelationEmptyConditionSchema(BaseModel):
    relation: str = Field(..., description="A relation defined in the blueprint")
    operator: Literal["isEmpty", "isNotEmpty"] = Field(..., description="Operator to use when evaluating this rule")
    not_: bool = Field(False, description="Negate the result of the rule")
