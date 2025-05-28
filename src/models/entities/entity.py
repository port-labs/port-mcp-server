"""Port.io entity model."""

from typing import Any, Literal

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.models.common.base_pydantic import BaseModel
from src.models.common.icon import Icon


class SearchRuleEquals(BaseModel):
    property: str = Field(..., description="The property of the entity")
    operator: Literal["="] = Field(..., description="The operator of the search rule")
    value: str | int = Field(..., description="The value of the search rule")


class SearchRuleIn(BaseModel):
    property: str = Field(..., description="The property of the entity")
    operator: Literal["in"] = Field(..., description="The operator of the search rule")
    value: list[str] = Field(..., description="The value of the search rule")


class SearchRuleQuery(BaseModel):
    combinator: Literal["and", "or"] = Field(..., description="The combinator of the search query")
    rules: list[SearchRuleEquals | SearchRuleIn] = Field(..., description="The conditions of the search query")


class SearchQuery(BaseModel):
    combinator: Literal["and", "or"] = Field(..., description="The combinator of the search query")
    rules: list[SearchRuleEquals | SearchRuleIn] = Field(..., description="The conditions of the search query")


class CommonEntity(BaseModel):
    """Data model for Port entity."""

    identifier: str | SearchQuery | SearchRuleIn | SearchRuleEquals | SkipJsonSchema[None] = Field(
        None,
        description="The identifier of the new entity. New entities must match the regex pattern: ^[A-Za-z0-9@_.:\\/=-]+$",
    )
    title: str | SkipJsonSchema[None] = Field(None, description="The title of the entity")
    icon: Icon | SkipJsonSchema[None] = Field(None, description="The icon of the entity")
    team: list[str] | str | SkipJsonSchema[None] = Field(None, description="The Port team/s to which the new entity will belong.")
    properties: dict[str, Any] | SkipJsonSchema[None] = Field(
        None,
        description='An object containing the properties of the new entity, in "key":"value" pairs where the key is the property\'s identifier, and the value is its value.',
    )
    relations: dict[str, Any] | SkipJsonSchema[None] = Field(
        None,
        description="""An object containing the relations of the new entity, in "key":"value" pairs where the key is the relation's identifier, and the value is the related entity's identifier. You can also use a search query to define relations based on a property of the related entity.""",
    )


class CreateEntity(CommonEntity):
    pass


class UpdateEntity(CommonEntity):
    pass


class EntityResult(CommonEntity):
    blueprint: str = Field(..., description="The blueprint of the entity")
    created_at: str | SkipJsonSchema[None] = Field(None, description="The created at date of the entity")
    created_by: str | SkipJsonSchema[None] = Field(None, description="The created by user of the entity")
    updated_at: str | SkipJsonSchema[None] = Field(None, description="The updated at date of the entity")
    updated_by: str | SkipJsonSchema[None] = Field(None, description="The updated by user of the entity")
