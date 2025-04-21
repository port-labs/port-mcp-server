from typing import Any, Dict
from loguru import logger
from src.mcp_server_port.models.blueprints import Blueprint
from src.mcp_server_port.models.tools.tool import Tool
from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import Field

class DeleteBlueprintToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to delete")


class DeleteBlueprintTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="delete_blueprint",
            description="Delete a blueprint using it's identifier",
            input_schema=DeleteBlueprintToolSchema,
            output_schema=Blueprint,
            function=self.delete_blueprint,
        )
        self.port_client = port_client

    async def delete_blueprint(self, props: DeleteBlueprintToolSchema) -> Dict[str, Any]:
        args = props.dict()
        logger.info(f"Deleting blueprint with identifier: {args.get('identifier')}")
        result = await self.port_client.delete_blueprint(props.dict(exclude_none=True,exclude_defaults=True,exclude_unset=True))
        return {"success": result}