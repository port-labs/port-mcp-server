import logging
import pyport
from typing import Dict, Any, Optional, Union, List
from ..models.models import PortAgentResponse, PortBlueprint, PortBlueprintList, PortEntity, PortEntityList, PortScorecard, PortScorecardList
from ..config import PORT_API_BASE
from .agent import PortAgentClient
from .blueprints import PortBlueprintClient
from .entities import PortEntityClient
from .scorecards import PortScorecardClient

logger = logging.getLogger(__name__)

class PortClient:
    """Client for interacting with the Port API."""
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, region: str = "EU", base_url: str = PORT_API_BASE):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        
        if not client_id or not client_secret:
            logger.warning("Port client initialized without credentials")
            self._client = None
            self.agent = None
            self.blueprints = None
            self.entities = None
            self.scorecards = None
        else:
            self._client = pyport.PortClient(client_id=client_id, client_secret=client_secret, us_region=(region == "US"))
            self.agent = PortAgentClient(self._client)
            self.blueprints = PortBlueprintClient(self._client)
            self.entities = PortEntityClient(self._client)
            self.scorecards = PortScorecardClient(self._client)

    async def trigger_agent(self, prompt: str) -> Dict[str, Any]:
        """Trigger the Port AI agent with a prompt."""
        return await self.agent.trigger_agent(prompt)
    
    async def get_invocation_status(self, identifier: str) -> PortAgentResponse:
        """Get the status of an AI agent invocation."""
        return await self.agent.get_invocation_status(identifier)
    
    # Blueprint methods
    
    async def get_blueprints(self) -> Union[PortBlueprintList, str]:
        """
        Get all blueprints from Port.
        
        Returns:
            PortBlueprintList: A list of blueprints
            str: Formatted text representation of blueprints if to_text=True
        """
        return await self.blueprints.get_blueprints()

    async def get_blueprint(self, blueprint_identifier: str) -> Union[PortBlueprint, str]:
        """
        Get a specific blueprint by identifier.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            
        Returns:
            PortBlueprint: The blueprint object
            str: Formatted text representation of the blueprint if to_text=True
        """
        return await self.blueprints.get_blueprint(blueprint_identifier)
    
    # Entity methods
    
    async def get_entities(self, blueprint_identifier: str) -> Union[PortEntityList, str]:
        """
        Get all entities for a specific blueprint.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            
        Returns:
            PortEntityList: A list of entities
            str: Formatted text representation of entities if to_text=True
        """
        return await self.entities.get_entities(blueprint_identifier)
    
    async def get_entity(self, blueprint_identifier: str, entity_identifier: str) -> Union[PortEntity, str]:
        """
        Get a specific entity by identifier.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            entity_identifier: The identifier of the entity
            
        Returns:
            PortEntity: The entity object
            str: Formatted text representation of the entity if to_text=True
        """
        return await self.entities.get_entity(blueprint_identifier, entity_identifier)
    
    async def create_entity(self, blueprint_identifier: str, entity_data: Dict[str, Any]) -> PortEntity:
        """
        Create a new entity for a blueprint.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            entity_data: Data for the entity to create
            
        Returns:
            PortEntity: The created entity
        """
        return await self.entities.create_entity(blueprint_identifier, entity_data)
    
    async def update_entity(self, blueprint_identifier: str, entity_identifier: str, entity_data: Dict[str, Any]) -> PortEntity:
        """
        Update an existing entity.
        
        Args:
            blueprint_identifier: The identifier of the blueprint
            entity_identifier: The identifier of the entity to update
            entity_data: Updated data for the entity
            
        Returns:
            PortEntity: The updated entity
        """
        return await self.entities.update_entity(blueprint_identifier, entity_identifier, entity_data)
        
    # Scorecard methods
    
    async def get_all_scorecards(self) -> Union[PortScorecardList, str]:
        """
        Get all scorecards from Port.
        
        Returns:
            PortScorecardList: A list of scorecards
        """
        return await self.scorecards.get_scorecards()
    
    async def get_scorecard_details(self, scorecard_id: str, blueprint_id: str = None) -> Union[PortScorecard, str]:
        """
        Get a specific scorecard by its identifier.
        
        Args:
            scorecard_id: The unique identifier of the scorecard
            blueprint_id: The identifier of the blueprint the scorecard belongs to
                         If not provided, will try to find it from the list of scorecards
            
        Returns:
            PortScorecard: The scorecard object
        """
        return await self.scorecards.get_scorecard(scorecard_id, blueprint_id)
    
    async def create_new_scorecard(self, blueprint_id: str, scorecard_data: Dict[str, Any]) -> PortScorecard:
        """
        Create a new scorecard.
        
        Args:
            blueprint_id: The identifier of the blueprint to create the scorecard for
            scorecard_data: Data for the scorecard to create
            
        Returns:
            PortScorecard: The created scorecard
        """
        return await self.scorecards.create_scorecard(blueprint_id, scorecard_data)
    
    async def delete_scorecard(self, scorecard_id: str, blueprint_id: str) -> bool:
        """
        Delete a scorecard by ID.
        
        Args:
            scorecard_id: The identifier of the scorecard to delete
            blueprint_id: The identifier of the blueprint the scorecard belongs to
            
        Returns:
            bool: True if deletion was successful
        """
        return await self.scorecards.delete_scorecard(scorecard_id, blueprint_id) 