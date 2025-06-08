from typing import Any

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.entities import EntityResult
from src.models.tools.tool import Tool


class DeleteEntityToolSchema(BaseModel):
    entity_identifier: str = Field(..., description="The identifier of the entity to delete")
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to delete the entity for")
    delete_dependents: bool = Field(
        default=False,
        description="If true, this call will also delete all of the entity's dependents",
    )
    run_id: str | SkipJsonSchema[None] = Field(default=None, description="The run_id of the action to delete the entity for")


class DeleteEntityTool(Tool[DeleteEntityToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="delete_entity",
            description="Delete an entity for a specific blueprint using its identifier",
            input_schema=DeleteEntityToolSchema,
            output_schema=EntityResult,
            annotations=Annotations(
                title="Delete Entity",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True,
            ),
            function=self.delete_entity,
        )
        self.port_client = port_client

    async def delete_entity(self, props: DeleteEntityToolSchema) -> dict[str, Any]:
        blueprint_identifier = props.blueprint_identifier
        entity_identifier = props.entity_identifier
        delete_dependents = props.delete_dependents

        result = await self.port_client.delete_entity(blueprint_identifier, entity_identifier, delete_dependents)

        return {"success": result}
