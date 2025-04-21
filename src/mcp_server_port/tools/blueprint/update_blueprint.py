from typing import Any, Dict
from loguru import logger
from src.mcp_server_port.models.blueprints import Blueprint
from src.mcp_server_port.models.blueprints import CreateBlueprint
from src.mcp_server_port.models.tools.tool import Tool
from src.mcp_server_port.client.client import PortClient

class UpdateBlueprintToolSchema(CreateBlueprint):
    pass


class UpdateBlueprintTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="update_blueprint",
            description="Update a blueprint using it's identifier",
            input_schema=UpdateBlueprintToolSchema,
            output_schema=Blueprint,
            function=self.update_blueprint,
        )
        self.port_client = port_client

    async def update_blueprint(self, props: UpdateBlueprintToolSchema) -> Dict[str, Any]:
        args = props.dict()
        logger.info(f"Updating blueprint with identifier: {args.get('identifier')}")
        blueprint = await self.port_client.update_blueprint(props.dict(exclude_none=True,exclude_defaults=True,exclude_unset=True))
        return blueprint.dict(exclude_unset=True, exclude_none=True)