from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field,TypeAdapter
from typing import Any, Dict, List, Union, Literal
from datetime import datetime
import json
class DateRange(BaseModel):
    from_date: datetime = Field(..., alias="from", description="The start date of the date range")
    to_date: datetime = Field(..., alias="to", description="The end date of the date range")

class BaseCondition(BaseModel):
    property: str = Field(..., description="The property to condition on")
    operator: str = Field(..., description="The operator to use for the condition")

class PropertyBetweenCondition(BaseCondition):
    operator: Literal["between", "notBetween"] = Field(..., description="The operator to use for the condition")
    value: DateRange = Field(..., description="The date range to use for the condition")

class PropertyContainsAnyCondition(BaseCondition):
    operator: Literal["containsAny"] = Field(..., description="The operator to use for the condition")
    value: List[str]

class PropertyComparisonCondition(BaseCondition):
    operator: Literal["=", "!=", ">", "<", ">=", "<=", "contains", 
                      "doesNotContains", "beginsWith", "doesNotBeginsWith",
                      "endsWith", "doesNotEndsWith"] = Field(..., description="The operator to use for the condition")
    value: Union[str, int, float, bool] = Field(..., description="The value to use for the condition")

class PropertyEmptyCondition(BaseCondition):
    operator: Literal["isEmpty", "isNotEmpty"] = Field(..., description="The operator to use for the condition")
    not_: bool = Field(default=False, alias="not", description="Whether to negate the condition")

# Condition union clearly describes polymorphism:
Condition = Union[
    PropertyBetweenCondition,
    PropertyContainsAnyCondition,
    PropertyComparisonCondition,
    PropertyEmptyCondition,
]

class ScorecardQuery(BaseModel):
    combinator: Literal["AND", "OR"] = Field(..., description="The combinator to use for the query")
    conditions: List[Condition] = Field(..., description="The conditions to use for the query")

class ScorecardRule(BaseModel):
    identifier: str = Field(..., max_length=20, pattern=r"^[A-Za-z0-9@_=\\-]+$", description="The identifier of the rule")
    title: str = Field(..., description="The title of the rule")
    level: Literal["Low", "Medium", "High", "Critical"] = Field(..., description="The level of the rule")
    query: ScorecardQuery = Field(..., description="The query to use for the rule")

class Scorecard(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint")
    identifier: str = Field(..., description="The identifier of the scorecard")
    title: str = Field(..., description="The title of the scorecard")
    levels: List[dict] = Field(..., description="The levels of the scorecard")
    rules: List[ScorecardRule] = Field(..., description="The rules of the scorecard")
    description: str = Field(..., description="The description of the scorecard")


# Generate the schema with refs
schema_with_refs = Scorecard.model_json_schema()

# Inline all refs
fully_inline_schema = inline_schema(schema_with_refs)

# Print the fully inlined schema
print(json.dumps(fully_inline_schema, indent=2))