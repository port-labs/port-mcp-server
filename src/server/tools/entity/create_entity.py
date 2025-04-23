from typing import Any, Dict
from loguru import logger
from src.server.models import Entity, CreateEntity, Annotations
from src.server.models.tools.tool import Tool
from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field
from src.server.client.client import PortClient
from pydantic.json_schema import SkipJsonSchema

class CreateEntitiyQuery(BaseModel):
    upsert: bool | SkipJsonSchema[None] = Field(default=False, description="If true, this call will override the entire entity if it already exists.")
    merge: bool | SkipJsonSchema[None] = Field(default=False, description="If true and upsert is also true, this call will update the entity if it already exists.")
    validation_only: bool | SkipJsonSchema[None] = Field(default=False, description="If true, this call will only validate the entity and return the validation errors.")
    create_missing_related_entities: bool | SkipJsonSchema[None] = Field(default=False, description="If true, this call will also create missing related entities. This is useful when you want to create an entity and its related entities in one call, or if you want to create an entity whose related entity does not exist yet.")
    run_id: str | SkipJsonSchema[None] = Field(default=None, description="You can provide a run_id to associate the created entity with a specific action run.")
    
class CreateEntityToolSchema(BaseModel):
    query: CreateEntitiyQuery  = Field(..., description="The query to create the entity")
    entity: CreateEntity = Field(..., description="The entity to create")
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to create the entity for")
class CreateEntityTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="create_entity",
            description="Create an entity which is an instance of a blueprint, it represents the data defined by a blueprint's properties.",
            input_schema=CreateEntityToolSchema,
            output_schema=Entity,
            annotations=Annotations(
                title="Create Entity",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True
            ),
            function=self.create_entity,
        )
        self.port_client = port_client

    async def create_entity(self, props: CreateEntityToolSchema) -> Dict[str, Any]:
        blueprint_identifier = props.blueprint_identifier

        logger.info(f"Creating entity for blueprint '{blueprint_identifier}' in Port")
        
        data = props.entity.model_dump(exclude_unset=True, exclude_none=True)
        query = props.query.model_dump(exclude_unset=True, exclude_none=True) or {}
        result = await self.port_client.create_entity(blueprint_identifier, data, query)
        result_dict = result.model_dump(exclude_unset=True, exclude_none=True)
        return result_dict
