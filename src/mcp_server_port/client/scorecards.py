import logging
from typing import Dict, List, Union, Any
from ..models.models import PortScorecard, PortScorecardList
from ..utils import PortError

logger = logging.getLogger(__name__)

class PortScorecardClient:
    """Client for interacting with Port Scorecard APIs."""
    
    def __init__(self, client):
        self._client = client

    async def get_scorecards(self) -> Union[PortScorecardList, str]:
        """
        Get all scorecards.
        
        Returns:
            PortScorecardList: A list of scorecards
        """
        if not self._client:
            raise PortError("Cannot get scorecards: Port client not initialized with credentials")
        
        try:
            logger.info("Getting all scorecards from Port")
            
            # Use the SDK's scorecard methods
            scorecards_data = self._client.scorecards.get_scorecards()
            scorecards = []
            
            for scorecard_data in scorecards_data:
                scorecard = PortScorecard(
                    identifier=scorecard_data.get("identifier", ""),
                    title=scorecard_data.get("title", "Untitled Scorecard"),
                    description=scorecard_data.get("description"),
                    blueprint=scorecard_data.get("blueprint", ""),
                    rules=scorecard_data.get("rules", []),
                    levels=scorecard_data.get("levels", []),
                    id=scorecard_data.get("id"),
                    calculation_method=scorecard_data.get("calculationMethod"),
                    created_at=scorecard_data.get("createdAt"),
                    created_by=scorecard_data.get("createdBy"),
                    updated_at=scorecard_data.get("updatedAt"),
                    updated_by=scorecard_data.get("updatedBy")
                )
                scorecards.append(scorecard)
            
            scorecard_list = PortScorecardList(
                scorecards=scorecards
            )
            return scorecard_list
            
        except Exception as e:
            logger.error(f"Error in get_scorecards: {str(e)}")
            # Check if this is an HTTP error and extract more details
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                status_code = e.response.status_code
                try:
                    # Try to extract the error message from the response JSON
                    error_data = e.response.json()
                    error_message = error_data.get('message', str(e))
                    if 'details' in error_data:
                        error_message += f". Details: {error_data['details']}"
                    
                    raise PortError(f"Error getting scorecards: {status_code} - {error_message}")
                except (ValueError, AttributeError):
                    # If we can't parse the JSON, just include the status code
                    raise PortError(f"Error getting scorecards: {status_code} - {str(e)}")
            else:
                raise PortError(f"Error getting scorecards: {str(e)}")
    
    async def get_scorecard(self, scorecard_id: str, blueprint_id: str = None) -> Union[PortScorecard, str]:
        """
        Get a specific scorecard by identifier.
        
        Args:
            scorecard_id: The identifier of the scorecard
            blueprint_id: The identifier of the blueprint the scorecard belongs to
                          If not provided, will try to find it from the list of scorecards
            
        Returns:
            PortScorecard: The scorecard object
        """
        if not self._client:
            raise PortError("Cannot get scorecard: Port client not initialized with credentials")
        
        try:
            # If blueprint_id is not provided, we need to fetch all scorecards and find the matching one
            if not blueprint_id:
                logger.info(f"Blueprint ID not provided, finding scorecard '{scorecard_id}' from all scorecards")
                scorecards = await self.get_scorecards()
                
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
            
            scorecard = PortScorecard(
                identifier=scorecard_data.get("identifier", ""),
                title=scorecard_data.get("title", "Untitled Scorecard"),
                description=scorecard_data.get("description"),
                blueprint=scorecard_data.get("blueprint", ""),
                rules=scorecard_data.get("rules", []),
                levels=scorecard_data.get("levels", []),
                id=scorecard_data.get("id"),
                calculation_method=scorecard_data.get("calculationMethod"),
                created_at=scorecard_data.get("createdAt"),
                created_by=scorecard_data.get("createdBy"),
                updated_at=scorecard_data.get("updatedAt"),
                updated_by=scorecard_data.get("updatedBy")
            )
            
            return scorecard
            
        except Exception as e:
            logger.error(f"Error in get_scorecard: {str(e)}")
            # Check if this is an HTTP error and extract more details
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                status_code = e.response.status_code
                try:
                    # Try to extract the error message from the response JSON
                    error_data = e.response.json()
                    error_message = error_data.get('message', str(e))
                    if 'details' in error_data:
                        error_message += f". Details: {error_data['details']}"
                    
                    raise PortError(f"Error getting scorecard '{scorecard_id}': {status_code} - {error_message}")
                except (ValueError, AttributeError):
                    # If we can't parse the JSON, just include the status code
                    raise PortError(f"Error getting scorecard '{scorecard_id}': {status_code} - {str(e)}")
            else:
                raise PortError(f"Error getting scorecard '{scorecard_id}': {str(e)}")
    
    async def create_scorecard(self, blueprint_id: str, scorecard_data: Dict[str, Any]) -> PortScorecard:
        """
        Create a new scorecard.
        
        Args:
            blueprint_id: The identifier of the blueprint to create the scorecard for
            scorecard_data: Data for the scorecard to create
            
        Returns:
            PortScorecard: The created scorecard
        """
        if not self._client:
            raise PortError("Cannot create scorecard: Port client not initialized with credentials")
        
        try:
            logger.info(f"Creating scorecard in blueprint '{blueprint_id}'")
            
            # Use direct API call with the correct URL format
            response = self._client.make_request("POST", f"blueprints/{blueprint_id}/scorecards", json=scorecard_data)
            created_data = response.json()
            
            # The API might return different formats for create operations
            if isinstance(created_data, dict) and "scorecard" in created_data:
                created_data = created_data.get("scorecard", {})
            
            created_scorecard = PortScorecard(
                identifier=created_data.get("identifier", ""),
                title=created_data.get("title", "Untitled Scorecard"),
                description=created_data.get("description"),
                blueprint=created_data.get("blueprint", blueprint_id),
                rules=created_data.get("rules", []),
                levels=created_data.get("levels", []),
                id=created_data.get("id"),
                calculation_method=created_data.get("calculationMethod"),
                created_at=created_data.get("createdAt"),
                created_by=created_data.get("createdBy"),
                updated_at=created_data.get("updatedAt"),
                updated_by=created_data.get("updatedBy")
            )
            
            return created_scorecard
            
        except Exception as e:
            logger.error(f"Error in create_scorecard: {str(e)}")
            # Check if this is an HTTP error and extract more details
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                status_code = e.response.status_code
                try:
                    # Try to extract the error message from the response JSON
                    error_data = e.response.json()
                    error_message = error_data.get('message', str(e))
                    if 'details' in error_data:
                        error_message += f". Details: {error_data['details']}"
                    
                    raise PortError(f"Error creating scorecard: {status_code} - {error_message}")
                except (ValueError, AttributeError):
                    # If we can't parse the JSON, just include the status code
                    raise PortError(f"Error creating scorecard: {status_code} - {str(e)}")
            else:
                raise PortError(f"Error creating scorecard: {str(e)}")
    
    async def delete_scorecard(self, scorecard_id: str, blueprint_id: str) -> bool:
        """
        Delete a scorecard by ID.
        
        Args:
            scorecard_id: The identifier of the scorecard to delete
            blueprint_id: The identifier of the blueprint the scorecard belongs to
            
        Returns:
            bool: True if deletion was successful
        """
        if not self._client:
            raise PortError("Cannot delete scorecard: Port client not initialized with credentials")
        
        try:
            logger.info(f"Deleting scorecard '{scorecard_id}' from blueprint '{blueprint_id}'")
            
            # Use direct API call with the correct URL format
            response = self._client.make_request("DELETE", f"blueprints/{blueprint_id}/scorecards/{scorecard_id}")
            
            # Check if the request was successful (204 No Content is common for DELETE operations)
            if response.status_code in (200, 202, 204):
                return True
            else:
                # Try to get the error message from the response, but handle the case where 
                # the response might not have a JSON body
                error_message = "Unknown error"
                try:
                    if hasattr(response, 'json') and callable(response.json):
                        response_json = response.json()
                        if isinstance(response_json, dict):
                            error_message = response_json.get('message', 'Unknown error')
                            # Add details if available
                            if 'details' in response_json:
                                error_message += f". Details: {response_json['details']}"
                except Exception:
                    # If we can't parse the json, just use the status code
                    error_message = f"HTTP {response.status_code}"
                    
                raise PortError(f"Error deleting scorecard: {response.status_code} - {error_message}")
            
        except Exception as e:
            logger.error(f"Error in delete_scorecard: {str(e)}")
            # Check if this is an HTTP error and extract more details
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                status_code = e.response.status_code
                try:
                    # Try to extract the error message from the response JSON
                    error_data = e.response.json()
                    error_message = error_data.get('message', str(e))
                    if 'details' in error_data:
                        error_message += f". Details: {error_data['details']}"
                    
                    raise PortError(f"Error deleting scorecard '{scorecard_id}': {status_code} - {error_message}")
                except (ValueError, AttributeError):
                    # If we can't parse the JSON, just include the status code
                    raise PortError(f"Error deleting scorecard '{scorecard_id}': {status_code} - {str(e)}")
            else:
                raise PortError(f"Error deleting scorecard '{scorecard_id}': {str(e)}") 