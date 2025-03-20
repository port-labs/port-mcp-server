import logging
from typing import Union
from ..models.models import PortBlueprint, PortBlueprintList
from ..utils import PortError

logger = logging.getLogger(__name__)

class PortBlueprintClient:
    """Client for interacting with Port Blueprint APIs."""
    
    def __init__(self, client):
        self._client = client

    async def get_blueprints(self) -> Union[PortBlueprintList, str]:
        """
        Get all blueprints from Port.
        
        Returns:
            PortBlueprintList: A list of blueprints
            str: Formatted text representation of blueprints if to_text=True
        """
        if not self._client:
            raise PortError("Cannot get blueprints: Port client not initialized with credentials")
        
        try:
            logger.info("Getting blueprints from Port")
            
            # Use the SDK's blueprints methods
            blueprints_data = self._client.blueprints.get_blueprints()
            blueprints = []
            
            for bp_data in blueprints_data:
                blueprint = PortBlueprint(
                    identifier=bp_data.get("identifier", ""),
                    title=bp_data.get("title", "Untitled Blueprint"),
                    description=bp_data.get("description"),
                    icon=bp_data.get("icon"),
                    schema=bp_data.get("schema"),
                    relations=bp_data.get("relations"),
                    created_at=bp_data.get("createdAt"),
                    created_by=bp_data.get("createdBy"),
                    updated_at=bp_data.get("updatedAt"),
                    updated_by=bp_data.get("updatedBy")
                )
                blueprints.append(blueprint)
            
            blueprint_list = PortBlueprintList(blueprints=blueprints)
            return blueprint_list
        
        except Exception as e:
            logger.error(f"Error in get_blueprints: {str(e)}")
            raise PortError(f"Error getting blueprints: {str(e)}")

    async def get_blueprint(self, blueprint_identifier: str) -> Union[PortBlueprint, str]:
        """
        Get a specific blueprint by identifier.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            
        Returns:
            PortBlueprint: The blueprint object
            str: Formatted text representation of the blueprint if to_text=True
        """
        if not self._client:
            raise PortError("Cannot get blueprint: Port client not initialized with credentials")
        
        try:
            logger.info(f"Getting blueprint '{blueprint_identifier}' from Port")
            
            # Use the SDK's blueprints methods
            bp_data = self._client.blueprints.get_blueprint(blueprint_identifier)
            
            blueprint = PortBlueprint(
                identifier=bp_data.get("identifier", ""),
                title=bp_data.get("title", "Untitled Blueprint"),
                description=bp_data.get("description"),
                icon=bp_data.get("icon"),
                schema=bp_data.get("schema"),
                relations=bp_data.get("relations"),
                created_at=bp_data.get("createdAt"),
                created_by=bp_data.get("createdBy"),
                updated_at=bp_data.get("updatedAt"),
                updated_by=bp_data.get("updatedBy")
            )
            
            return blueprint
            
        except Exception as e:
            logger.error(f"Error in get_blueprint: {str(e)}")
            raise PortError(f"Error getting blueprint '{blueprint_identifier}': {str(e)}") 