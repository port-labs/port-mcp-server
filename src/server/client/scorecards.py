import logging
import json
from typing import Any, Dict, Union

from pydantic import ValidationError

import requests
from src.server.models.scorecards import ScorecardCreate
from src.server.models import Scorecard
from src.server.utils import PortError
from pyport import PortClient
logger = logging.getLogger(__name__)

class PortScorecardClient:
    """Client for interacting with Port Scorecard APIs."""
    
    def __init__(self, client:PortClient):
        self._client = client

    async def get_scorecards(self, blueprint_identifier: str) -> Union[list[Scorecard], str]:
        if not self._client:
            raise PortError("Cannot get scorecards: Port client not initialized with credentials")
    
        logger.info("Getting all scorecards from Port")
        
        # Use the SDK's scorecard methods
        scorecards_data = self._client.scorecards.get_scorecards(blueprint_identifier)

        return [Scorecard(**scorecard_data) for scorecard_data in scorecards_data]
        
    
    async def get_scorecard(self, scorecard_id: str, blueprint_id: str = None) -> Union[Scorecard, str]:
        if not self._client:
            raise PortError("Cannot get scorecard: Port client not initialized with credentials")
        
        if not blueprint_id:
            logger.info(f"Blueprint ID not provided, finding scorecard '{scorecard_id}' from all scorecards")
            scorecards = await self.get_scorecards(blueprint_id)
            
            # Find the scorecard with matching identifier
            for scorecard in scorecards.scorecards:
                if scorecard.identifier == scorecard_id:
                    blueprint_id = scorecard.blueprint
                    break
                    
            if not blueprint_id:
                raise PortError(f"Could not find blueprint for scorecard '{scorecard_id}'")
        
        logger.info(f"Getting scorecard '{scorecard_id}' from blueprint '{blueprint_id}'")
        
        # Use direct API call with the correct URL format
        response = self._client.make_request("GET", f"blueprints/{blueprint_id}/scorecards/{scorecard_id}")
        scorecard_data = response.json()
        
        # The API returns the scorecard object nested under a 'scorecard' key
        if isinstance(scorecard_data, dict) and "scorecard" in scorecard_data:
            scorecard_data = scorecard_data.get("scorecard", {})
        
        return Scorecard(**scorecard_data)
            
    async def create_scorecard(self, blueprint_id: str, scorecard_data: Dict[str, Any]) -> Scorecard:
        if not self._client:
            raise PortError("Cannot create scorecard: Port client not initialized with credentials")
        
        logger.info(f"Creating scorecard in blueprint '{blueprint_id}'")
        json_data = json.dumps(scorecard_data)
        logger.info(f"Data: {json_data}")

        response = self._client.make_request("POST", f"blueprints/{blueprint_id}/scorecards", json=scorecard_data)

        created_data = response.json()
        logger.info(f"Created data: {created_data}")

        data = created_data.get("scorecard", {})
        
        return Scorecard(**data)
            
    async def delete_scorecard(self, scorecard_id: str, blueprint_id: str) -> bool:
        if not self._client:
            raise PortError("Cannot delete scorecard: Port client not initialized with credentials")
        
        logger.info(f"Deleting scorecard '{scorecard_id}' from blueprint '{blueprint_id}'")
        
        response = self._client.make_request("DELETE", f"blueprints/{blueprint_id}/scorecards/{scorecard_id}")
        logger.info(f"Response: {response}")
        return True
    
    async def update_scorecard(self, blueprint_id: str, scorecard_data: Dict[str, Any]) -> Scorecard:
        if not self._client:
            raise PortError("Cannot update scorecard: Port client not initialized with credentials")
        
        logger.info(f"Updating scorecard '{scorecard_data.get('identifier', 'No identifier provided')}' in blueprint '{blueprint_id}'")
        
        response = self._client.make_request("PUT", f"blueprints/{blueprint_id}/scorecards/{scorecard_data['identifier']}", json=scorecard_data)

        updated_data = response.json()
        logger.info(f"Updated data: {updated_data}")
        if updated_data.get("ok"):
            data = updated_data.get("scorecard", {})
            return Scorecard(**data)
        else:
            raise PortError(f"Error updating scorecard: {updated_data.get('error', 'Unknown error')}")
