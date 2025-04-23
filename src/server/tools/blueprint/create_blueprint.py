from typing import Any, Dict
from loguru import logger
from src.server.models import Annotations, Blueprint, CreateBlueprint
from src.server.models.tools.tool import Tool
from src.server.client.client import PortClient

class CreateBlueprintToolSchema(CreateBlueprint):
    pass    
class CreateBlueprintTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="create_blueprint",
            description="Create blueprints which are the most basic building block in Port. They are used to represent assets in your organization, and the relationships between them.",
            input_schema=CreateBlueprintToolSchema,
            output_schema=Blueprint,
            annotations=Annotations(
                title="Create Blueprint",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=False,
                openWorldHint=True
            ),
            function=self.create_blueprint,
        )
        self.port_client = port_client

    async def create_blueprint(self, props: CreateBlueprintToolSchema) -> Dict[str, Any]:
        blueprint = await self.port_client.create_blueprint(props.model_dump(exclude_none=True,exclude_defaults=True,exclude_unset=True))
        blueprint_dict = blueprint.model_dump(exclude_unset=True, exclude_none=True)
        return blueprint_dict