import datetime
from typing import List, Literal, Union, Annotated

from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field
from pydantic import field_serializer
from pydantic.json_schema import SkipJsonSchema

class ScorecardLevelSchema(BaseModel):
    title: str = Field(..., description="The title of the level to create")
    color: Literal["blue", "turquoise", "orange", "purple", "pink", "yellow", "green", "red", "gold", "silver", "paleBlue", "darkGray", "lightGray", "bronze"] = Field(..., description="The color of the level to create")

#****
class DateRangeSchema(BaseModel):
    from_date: datetime.datetime = Field(..., description="The start date of the range",alias="from")
    to_date: datetime.datetime = Field(..., description="The end date of the range",alias="to")
class DatePresetSchema(BaseModel):
    preset: Literal["today", "tomorrow", "yesterday", "lastWeek", "last2Weeks", "lastMonth", "last3Months", "last6Months", "last12Months"] = Field(..., description="Presets of date ranges")

class ScorecardConditionPropertyBetweenConditionSchema(BaseModel):
    conditionName: Literal["propertyBetween"] = Field(..., description="Must be set to identify the condition type and use it")
    property: str = Field(..., description="Date property to filter by according to its value")
    operator: Literal["between", "notBetween", "="] = Field(..., description="Operator to use when evaluating this rule")
    value: Union[DateRangeSchema, DatePresetSchema] = Field(..., description="Date value to compare to")
#****
class ScorecardConditionPropertyContainsAnyConditionSchema(BaseModel):
    conditionName: Literal["propertyContainsAny"] = Field(..., description="Must be set to identify the condition type and use it")
    property: str = Field(..., description="Property to filter by according to its value")
    operator: Literal["containsAny"] = Field(..., description="Operator eveluates if the property contains any of the values in the list")
    value: List[str] = Field(..., description="List of values to compare to")
#****
class ScorecardConditionRelationComparisonConditionSchema(BaseModel):
    conditionName: Literal["relationComparison"] = Field(..., description="Must be set to identify the condition type and use it")
    relation: str = Field(..., description="The relation of the condition to create")
    operator: Literal["=", "!=", "contains", "doesNotContains", "beginsWith", "doesNotBeginsWith", "endsWith", "doesNotEndsWith"] = Field(..., description="Operator to use when evaluating this rule")
    value: Union[str,int,float,bool] = Field(..., description="Value to compare to")
#****
class ScorecardConditionPropertyComparisonConditionSchema(BaseModel):
    conditionName: Literal["propertyComparison"] = Field(..., description="Must be set to identify the condition type and use it")
    property: str = Field(..., description="Property to filter by according to its value")
    operator: Literal["=", "!=", ">", "<", ">=", "<=", "contains", "doesNotContains", "beginsWith", "doesNotBeginsWith", "endsWith", "doesNotEndsWith"] = Field(..., description="Operator to use when evaluating this rule")
    value: Union[str,int,bool] = Field(..., description="Value to compare to")
#****
class ScorecardConditionPropertyEmptyConditionSchema(BaseModel):
    conditionName: Literal["propertyEmpty"] = Field(..., description="Must be set to identify the condition type and use it")
    property: str = Field(..., description="Property to filter by according to its value")
    operator: Literal["isEmpty", "isNotEmpty"] = Field(..., description="Operator to use when evaluating this rule")
    not_: bool = Field(False, description="Negate the result of the rule")
#****
class ScorecardConditionRelationEmptyConditionSchema(BaseModel):
    conditionName: Literal["relationEmpty"] = Field(..., description="Must be set to identify the condition type and use it")
    relation: str = Field(..., description="The relation of the condition to create")
    operator: Literal["isEmpty", "isNotEmpty"] = Field(..., description="Operator to use when evaluating this rule")
    not_: bool = Field(False, description="Negate the result of the rule")
#****




class ScorecardQuerySchema(BaseModel):
    combinator: Literal["and", "or"] = Field(..., description="The combinator of the rule to create")
    conditions: List[Union[
        ScorecardConditionPropertyBetweenConditionSchema,
        ScorecardConditionPropertyContainsAnyConditionSchema,
        ScorecardConditionPropertyEmptyConditionSchema,
        ScorecardConditionRelationEmptyConditionSchema,
        ScorecardConditionRelationComparisonConditionSchema,
        ScorecardConditionPropertyComparisonConditionSchema
    ]] = Field(..., description="Pay extreme attention to the conditions schema and the required fields, they are small boolean checks that help when determining the final status of a query according to the specified combinator")


class ScorecardRuleSchema(BaseModel):
    identifier: str = Field(..., pattern=r'^[A-Za-z0-9@_.:\\/=-]+$', max_length=20,description="The identifier of the rule to create")
    title: str = Field(..., description="The title of the rule to create")
    level: str = Field(..., description="The level of the rule to create, must be a valid level - cant be the first level in the scorecard")
    query: ScorecardQuerySchema = Field(..., description="The query of the rule to create")
    description: str = Field(..., description="The description of the rule to create")
