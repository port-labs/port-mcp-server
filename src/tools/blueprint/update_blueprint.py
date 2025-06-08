from typing import Any

from src.client.client import PortClient
from src.models.blueprints import Blueprint, UpdateBlueprint
from src.models.common.annotations import Annotations
from src.models.tools.tool import Tool
from src.utils import logger


class UpdateBlueprintToolSchema(UpdateBlueprint):
    pass


class UpdateBlueprintTool(Tool[UpdateBlueprintToolSchema]):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_blueprint",
            description="Update a blueprint using its identifier",
            input_schema=UpdateBlueprintToolSchema,
            output_schema=Blueprint,
            annotations=Annotations(
                title="Update Blueprint",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True,
            ),
            function=self.update_blueprint,
        )
        self.port_client = port_client

    async def update_blueprint(self, props: UpdateBlueprintToolSchema) -> dict[str, Any]:
        args = props.model_dump(exclude_unset=True, exclude_none=True)
        identifier = args.get("identifier")
        logger.info(f"Updating blueprint with identifier: {identifier}")

        blueprint = await self.port_client.update_blueprint(args)
        blueprint_dict = blueprint.model_dump(exclude_unset=True, exclude_none=True)
        return blueprint_dict
