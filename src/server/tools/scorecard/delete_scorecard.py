from loguru import logger
from src.server.models import Annotations
from src.server.models.tools.tool import Tool  
from src.server.client.client import PortClient
from src.server.models.common.base_pydantic import BaseModel
from pydantic import Field
from typing import Any, Dict

class DeleteScorecardToolSchema(BaseModel):
    blueprint_identifier: str = Field(..., description="The identifier of the blueprint to get scorecard for")
    scorecard_identifier: str = Field(..., description="The identifier of the scorecard to get")

class DeleteScorecardToolResponse(BaseModel):
    success: bool = Field(..., description="Whether the scorecard was deleted successfully")
    message: str = Field(..., description="The message from the operation")

class DeleteScorecardTool(Tool):
    port_client: PortClient

    def __init__(self, port_client: PortClient):
        super().__init__(
            name="delete_scorecard",
            description="Delete a scorecard from a given blueprint using it's identifier",
            input_schema=DeleteScorecardToolSchema,
            output_schema=DeleteScorecardToolResponse,
            annotations=Annotations(
                title="Delete Scorecard",
                readOnlyHint=False,
                destructiveHint=True,
                idempotentHint=False,
                openWorldHint=True
            ),
            function=self.delete_scorecard,
        )
        self.port_client = port_client

    async def delete_scorecard(self, props: DeleteScorecardToolSchema) -> Dict[str, Any]:
        args = props.model_dump()
        scorecard_id = args.get("scorecard_identifier")
        blueprint_id = args.get("blueprint_identifier")
        
        logger.info(f"Deleting scorecard '{scorecard_id}' from blueprint '{blueprint_id}'")
        
        # First verify that the scorecard exists
        try:
            await self.port_client.get_scorecard(scorecard_id, blueprint_id)
        except Exception as e:
            logger.warning(f"Scorecard '{scorecard_id}' not found or not accessible: {str(e)}")
            raise Exception(f"❌ Cannot delete scorecard '{scorecard_id}': Scorecard not found or not accessible")
        
        # Delete the scorecard
        result = await self.port_client.delete_scorecard(scorecard_id, blueprint_id)
        
        if result:
            return DeleteScorecardToolResponse(success=True, message=f"✅ Successfully deleted scorecard '{scorecard_id}' from blueprint '{blueprint_id}'").model_dump()
        else:
            return DeleteScorecardToolResponse(success=False, message=f"❌ Failed to delete scorecard '{scorecard_id}'. No error was reported, but the operation may not have succeeded.").model_dump()
