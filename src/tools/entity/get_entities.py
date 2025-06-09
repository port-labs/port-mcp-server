from typing import Any

from pydantic import Field

from src.client.client import PortClient
from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.entities import EntityResult
from src.models.tools.tool import Tool


class GetEntitiesToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get entities for")
    detailed: bool = Field(
        default=False,
        description="If True, returns complete entity details including properties. If False (default), returns summary information only.",
    )


class GetEntitiesToolResponse(BaseModel):
    entities: list[EntityResult] = Field(..., description="The list of entities")


class GetEntitiesTool(Tool[GetEntitiesToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="get_entities",
            description="Get all of the entities for a given blueprint",
            input_schema=GetEntitiesToolSchema,
            output_schema=GetEntitiesToolResponse,
            annotations=Annotations(
                title="Get Entities",
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            function=self.get_entities,
        )
        self.port_client = port_client

    async def get_entities(self, props: GetEntitiesToolSchema) -> dict[str, Any]:
        args = props.model_dump()

        blueprint_identifier = args.get("blueprint_identifier")
        if not blueprint_identifier:
            raise ValueError("Blueprint identifier is required")

        raw_entities = await self.port_client.get_entities(blueprint_identifier)
        processed_entities = [entity.model_dump(exclude_unset=True, exclude_none=True) for entity in raw_entities]

        response = GetEntitiesToolResponse.construct(entities=processed_entities)
        return response.model_dump(exclude_unset=True, exclude_none=True)
