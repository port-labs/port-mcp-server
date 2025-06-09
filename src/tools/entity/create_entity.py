from typing import Any

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.entities import CreateEntity, EntityResult
from src.models.tools.tool import Tool


class CreateEntitiyQuery(BaseModel):
    upsert: bool | SkipJsonSchema[None] = Field(
        default=True,
        description="If true, this call will override the entire entity if it already exists.",
    )
    merge: bool | SkipJsonSchema[None] = Field(
        default=True,
        description="If true and upsert is also true, this call will update the entity if it already exists.",
    )
    validation_only: bool | SkipJsonSchema[None] = Field(
        default=False,
        description="If true, this call will only validate the entity and return the validation errors.",
    )
    create_missing_related_entities: bool | SkipJsonSchema[None] = Field(
        default=False,
        description="If true, this call will also create missing related entities. This is useful when you want to create an entity and its related entities in one call, or if you want to create an entity whose related entity does not exist yet.",
    )
    run_id: str | SkipJsonSchema[None] = Field(
        default=None,
        description="You can provide a run_id to associate the created entity with a specific action run.",
    )


class CreateEntityToolSchema(BaseModel):
    query: CreateEntitiyQuery = Field(..., description="The query to create the entity")
    entity: CreateEntity = Field(..., description="The entity to create")
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to create the entity for")


class CreateEntityTool(Tool[CreateEntityToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="create_entity",
            description="Create an entity which is an instance of a blueprint, it represents the data defined by a blueprint's properties.",
            input_schema=CreateEntityToolSchema,
            output_schema=EntityResult,
            annotations=Annotations(
                title="Create Entity",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True,
            ),
            function=self.create_entity,
        )
        self.port_client = port_client

    async def create_entity(self, props: CreateEntityToolSchema) -> dict[str, Any]:
        blueprint_identifier = props.blueprint_identifier

        data = props.entity.model_dump(exclude_unset=True, exclude_none=True)
        query = props.query.model_dump(exclude_unset=True, exclude_none=True) or {}

        result = await self.port_client.create_entity(blueprint_identifier, data, query)
        result_dict = result.model_dump(exclude_unset=True, exclude_none=True)

        return result_dict
