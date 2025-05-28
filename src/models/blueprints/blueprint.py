"""Port.io blueprint model."""

from typing import Any, Literal

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.models.common.base_pydantic import BaseModel
from src.models.common.icon import Icon


class PropertySchema(BaseModel):
    title: str = Field(..., description="The title of the property")
    description: str | SkipJsonSchema[None] = Field(None, description="The description of the property")
    icon: Icon | SkipJsonSchema[None] = Field(None, description="The icon of the property")
    type: Literal["string", "number", "boolean", "object", "array"] = Field(..., description="The type of the property")
    format: (
        Literal[
            "date-time",
            "url",
            "email",
            "ipv4",
            "ipv6",
            "markdown",
            "yaml",
            "user",
            "team",
            "timer",
            "proto",
        ]
        | SkipJsonSchema[None]
    ) = Field(None, description="The format of the property")
    spec: Literal["open-api", "embedded-url", "async-api"] | SkipJsonSchema[None] = Field(
        None, description="The spec of the property"
    )


class BluePrintSchema(BaseModel):
    properties: dict[str, PropertySchema] = Field(
        ...,
        description="Properties are customizable data fields of blueprints, used to save and display information from external data sources.",
    )
    required: list[str] = Field(
        ...,
        description="The required properties of the blueprint, these must be provided when creating an entity based on this blueprint. This is an array of the required properties' identifiers.",
    )


class CalculationProperyItemsSchema(BaseModel):
    type: Literal["string", "number", "boolean", "object", "array"] = Field(
        ..., description="The type of the calculation property"
    )
    format: (
        Literal[
            "date-time",
            "url",
            "email",
            "ipv4",
            "ipv6",
            "markdown",
            "yaml",
            "user",
            "team",
            "timer",
            "proto",
        ]
        | SkipJsonSchema[None]
    ) = Field(None, description="The format of the calculation property")


class CalculationPropertiesSchema(BaseModel):
    title: str | SkipJsonSchema[None] = Field(None, description="The title of the calculation property")
    description: str | SkipJsonSchema[None] = Field(None, description="The description of the calculation property")
    icon: Icon | SkipJsonSchema[None] = Field(None, description="The icon of the calculation property")
    calculation: str = Field(..., description="The jq expression to transform properties into a calculation")
    type: Literal["string", "number", "boolean", "object", "array"] = Field(
        ..., description="The type of the calculation property"
    )
    format: (
        Literal["date-time", "url", "email", "ipv4", "ipv6", "markdown", "yaml", "user", "team", "proto"] | SkipJsonSchema[None]
    ) = Field(None, description="The format of the calculation property")
    spec: Literal["open-api", "embedded-url", "async-api"] | SkipJsonSchema[None] = Field(
        None, description="The spec of the calculation property"
    )
    colorized: bool | SkipJsonSchema[None] = Field(
        None,
        description="Boolean flag to define whether the calculation property should be colorized",
    )
    colors: dict[str, Any] | SkipJsonSchema[None] = Field(None, description="The color of the calculation property")
    items: CalculationProperyItemsSchema | SkipJsonSchema[None] = Field(None, description="The items of the calculation property")


class MirrorPropertiesSchema(BaseModel):
    title: str = Field(..., description="The title of the mirror property")
    path: str = Field(..., description="The path of the mirror property - relationName.propertyName")


class RelationSchema(BaseModel):
    title: str | SkipJsonSchema[None] = Field(..., description="The name of the relation")
    description: str | SkipJsonSchema[None] = Field(None, description="The description of the relation")
    target: str = Field(
        ...,
        description="Target blueprint identifier, the target blueprint has to exist when defining the relation",
    )
    required: bool = Field(
        ...,
        description="Boolean flag to define whether the target must be provided when creating a new entity of the blueprint	",
    )
    many: bool = Field(
        ...,
        description="Boolean flag to define whether multiple target entities can be mapped to the Relation",
    )


class AggregationPropertiesSchema(BaseModel):
    title: str = Field(..., description="The title of the aggregation property")
    description: str | SkipJsonSchema[None] = Field(None, description="The description of the aggregation property")
    icon: Icon | SkipJsonSchema[None] = Field(None, description="The icon of the aggregation property")
    type: Literal["number"] | SkipJsonSchema[None] = Field(None, description="The type of the aggregation property")
    target: str = Field(..., description="The target blueprint identifier")
    calculation_spec: dict[str, Any] = Field(
        ...,
        description="The functions to transform properties into an aggregation",
        alias="calculationSpec",
        serialization_alias="calculationSpec",
    )
    query: dict[str, Any] | SkipJsonSchema[None] = Field(None, description="The query to get the aggregation")


class TeamInheritanceSchema(BaseModel):
    path: str = Field(
        ...,
        description="path is the path to the desired blueprint via relations, for example: relationIdentifier.relationIdentifierInRelatedBlueprint",
    )


class BlueprintCommon(BaseModel):
    identifier: str = Field(
        ...,
        max_length=30,
        pattern=r"^[A-Za-z0-9@_.:\\/=-]+$",
        description="The unique identifier of the blueprint",
    )
    title: str = Field(..., max_length=30, description="The title of the blueprint")
    icon: Icon = Field("Template", description="The icon of the blueprint")
    blueprint_schema: BluePrintSchema = Field(
        ..., description="The schema of the blueprint", alias="schema", serialization_alias="schema"
    )
    calculation_properties: dict[str, CalculationPropertiesSchema] = Field(
        {},
        description="Calculation properties allow you to use existing properties defined on blueprints, either directly or by using relations and mirror properties, in order to create new properties by using the jq processor for JSON",
        alias="calculationProperties",
        serialization_alias="calculationProperties",
    )
    aggregation_properties: dict[str, AggregationPropertiesSchema] = Field(
        {},
        description="Aggregation properties allow you to aggregate data from related entities to your entity. Aggregation property can be used for blueprints that have relations defined.",
        alias="aggregationProperties",
        serialization_alias="aggregationProperties",
    )
    mirror_properties: dict[str, MirrorPropertiesSchema] = Field(
        {},
        description="Mirror property allows you to map data from related entities to your entity. Mirror property can be used for blueprints that have relations defined.",
        alias="mirrorProperties",
        serialization_alias="mirrorProperties",
    )
    relations: dict[str, RelationSchema] = Field(
        {},
        description="Relations define connections between blueprints, consequently connecting the entities based on these blueprints. This provides logical context to the software catalog.",
        serialization_alias="relations",
    )


class Blueprint(BlueprintCommon):
    created_at: str | SkipJsonSchema[None] = Field(None, description="The created at date of the blueprint")
    created_by: str | SkipJsonSchema[None] = Field(None, description="The created by user of the blueprint")
    updated_at: str | SkipJsonSchema[None] = Field(None, description="The updated at date of the blueprint")
    updated_by: str | SkipJsonSchema[None] = Field(None, description="The updated by user of the blueprint")


class CreateBlueprint(BlueprintCommon):
    team_inheritance: TeamInheritanceSchema | SkipJsonSchema[None] = Field(
        None,
        description="A relation to another blueprint from which to inherit the team. Can be any blueprint connected to this one via any number of relations.",
        alias="teamInheritance",
    )
    changelog_destination: dict[str, Any] | SkipJsonSchema[None] = Field(
        None,
        description="The destination of the changelog",
        alias="changelogDestination",
        serialization_alias="changelogDestination",
    )


class UpdateBlueprint(BlueprintCommon):
    pass
