from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.entities import CreateEntity, EntityResult
from src.models.tools.tool import Tool


class UpdateEntityToolSchema(BaseModel):
    entity_identifier: str = Field(..., description="The identifier of the entity to update")
    entity: CreateEntity = Field(..., description="The entity to update")
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to update the entity for")


class UpdateEntityTool(Tool[UpdateEntityToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_entity",
            description="Update an entity for a specific blueprint using its identifier. Preforms PUT-like replacement of the entity based on the provided payload and requires all required fields.",
            input_schema=UpdateEntityToolSchema,
            output_schema=EntityResult,
            annotations=Annotations(
                title="Update Entity",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True,
            ),
            function=self.update_entity,
        )
        self.port_client = port_client

    async def update_entity(self, props: UpdateEntityToolSchema) -> dict[str, Any]:
        blueprint_identifier = props.blueprint_identifier
        entity_identifier = props.entity_identifier

        data = props.entity.model_dump(exclude_unset=True, exclude_none=True)

        result = await self.port_client.update_entity(blueprint_identifier, entity_identifier, data)
        result_dict = result.model_dump(exclude_unset=True, exclude_none=True)

        return result_dict
