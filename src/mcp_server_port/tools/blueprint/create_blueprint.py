from typing import Any, Dict
from loguru import logger
from src.mcp_server_port.models.blueprints import Blueprint
from src.mcp_server_port.models.blueprints import CreateBlueprint
from src.mcp_server_port.models.tools.tool import Tool
from src.mcp_server_port.client.client import PortClient

class CreateBlueprintToolSchema(CreateBlueprint):
    pass


class CreateBlueprintTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="create_blueprint",
            description="Blueprints are the most basic building block in Port. They are used to represent assets in your organization, and the relationships between them.",
            input_schema=CreateBlueprintToolSchema,
            output_schema=Blueprint,
            function=self.create_blueprint,
        )
        self.port_client = port_client

    async def create_blueprint(self, props: CreateBlueprintToolSchema) -> Dict[str, Any]:
        args = props.dict()
        logger.info(f"Creating blueprint with identifier: {args.get('identifier')}")
        blueprint = await self.port_client.create_blueprint(props.dict(exclude_none=True,exclude_defaults=True,exclude_unset=True))
        return blueprint.dict(exclude_unset=True, exclude_none=True)