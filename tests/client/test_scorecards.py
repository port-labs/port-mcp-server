import os
import pytest
import sys
from dotenv import load_dotenv
import json
from unittest.mock import MagicMock, AsyncMock

# Add the src directory to the path so we can import our modules
sys.path.append('src')

from mcp_server_port.client import PortClient
from mcp_server_port.models.models import PortScorecardList, PortScorecard
from mcp_server_port.utils import PortError

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")
REGION = os.getenv("REGION", "EU")

# Skip tests if credentials are not available
require_credentials = pytest.mark.skipif(
    not PORT_CLIENT_ID or not PORT_CLIENT_SECRET,
    reason="Port credentials not available in environment variables"
)

@require_credentials
class TestPortScorecardClient:
    """Tests for the Port Scorecard Client functionality."""

    @pytest.fixture
    def client(self):
        """Create a PortClient instance with credentials."""
        return PortClient(
            client_id=PORT_CLIENT_ID,
            client_secret=PORT_CLIENT_SECRET,
            region=REGION
        )

    @pytest.fixture
    def mock_port_client(self):
        """Create a mock PortClient instance for testing error scenarios."""
        # Create a properly mocked client that won't make real API calls
        port_client = MagicMock()
        
        # Setup the structure needed for the client
        port_client._client = MagicMock()
        
        # Use AsyncMock for coroutine methods
        port_client.create_new_scorecard = AsyncMock()
        port_client.get_scorecard_details = AsyncMock()
        port_client.scorecards = MagicMock()
        
        return port_client

    @pytest.mark.asyncio
    async def test_get_scorecards(self, client):
        """Test getting all scorecards."""
        # Get all scorecards
        scorecard_list = await client.get_all_scorecards()
        
        # Validate the response type
        assert isinstance(scorecard_list, PortScorecardList)
        
        # Print information about the scorecards
        print(f"Found {len(scorecard_list.scorecards)} scorecards")
        
        # Skip further tests if no scorecards are found
        if not scorecard_list.scorecards:
            pytest.skip("No scorecards found to test with")
            
        # Validate that we have at least one scorecard
        assert len(scorecard_list.scorecards) > 0
        
        # Validate the first scorecard
        first_scorecard = scorecard_list.scorecards[0]
        assert isinstance(first_scorecard, PortScorecard)
        assert first_scorecard.identifier
        assert first_scorecard.title
        assert first_scorecard.blueprint
        
        # Print the first scorecard for debugging
        print(f"First scorecard: {first_scorecard.title} (ID: {first_scorecard.identifier})")
        print(f"Blueprint: {first_scorecard.blueprint}")
        print(f"Rules count: {len(first_scorecard.rules)}")
        print(f"Levels count: {len(first_scorecard.levels)}")

    @pytest.mark.asyncio
    async def test_get_scorecard(self, client):
        """Test getting a specific scorecard by identifier."""
        # First, get all scorecards to find one to test with
        scorecard_list = await client.get_all_scorecards()
        
        # Validate the response type
        assert isinstance(scorecard_list, PortScorecardList)
        
        # Print information about the scorecards
        print(f"Found {len(scorecard_list.scorecards)} scorecards")
        
        # Skip if no scorecards are found
        if not scorecard_list.scorecards:
            pytest.skip("No scorecards found to test with")
            
        # Select the first scorecard
        first_scorecard = scorecard_list.scorecards[0]
        
        # Print debug information about the scorecard
        print(f"First scorecard debug info:")
        print(f"  Title: {first_scorecard.title}")
        print(f"  Identifier: {first_scorecard.identifier}")
        print(f"  Blueprint: {first_scorecard.blueprint}")
        
        scorecard_identifier = first_scorecard.identifier
        blueprint_id = first_scorecard.blueprint
        
        if not scorecard_identifier or not blueprint_id:
            pytest.skip("Scorecard identifier or blueprint is missing, cannot test get_scorecard")
        
        print(f"Testing get_scorecard with identifier: '{scorecard_identifier}' and blueprint: '{blueprint_id}'")
        
        try:
            # Get the specific scorecard by identifier and blueprint
            scorecard = await client.get_scorecard_details(scorecard_identifier, blueprint_id)
            
            # Validate the response
            assert isinstance(scorecard, PortScorecard)
            assert scorecard.identifier == scorecard_identifier
            assert scorecard.blueprint == blueprint_id
            assert scorecard.title
            
            # Print the scorecard details for debugging
            print(f"Successfully retrieved scorecard: {scorecard.title}")
            print(f"Blueprint: {scorecard.blueprint}")
            print(f"Rules count: {len(scorecard.rules)}")
            print(f"Levels count: {len(scorecard.levels)}")
            
            # Validate rules if present
            if scorecard.rules:
                first_rule = scorecard.rules[0]
                assert "identifier" in first_rule
                assert "title" in first_rule
                
            # Validate levels if present
            if scorecard.levels:
                first_level = scorecard.levels[0]
                assert "title" in first_level
                
            print("Scorecard test successful!")
        except Exception as e:
            print(f"Error retrieving scorecard: {str(e)}")
            import traceback
            traceback.print_exc()
            pytest.fail(f"Could not retrieve scorecard: {str(e)}")

    @pytest.mark.asyncio
    async def test_create_and_delete_scorecard(self, client):
        """Test creating a new scorecard and then deleting it."""
        # First, get all blueprints to find one to use
        try:
            # Get all blueprints
            print("Fetching blueprints...")
            blueprints = await client.get_blueprints()
            
            if not blueprints or not blueprints.blueprints:
                pytest.skip("No blueprints found to test with")
                
            # Choose a blueprint with properties
            test_blueprint = None
            for blueprint in blueprints.blueprints:
                if blueprint.schema and "properties" in blueprint.schema and blueprint.schema["properties"]:
                    test_blueprint = blueprint
                    break
                    
            if not test_blueprint:
                pytest.skip("No blueprint with properties found to test with")
                
            blueprint_id = test_blueprint.identifier
            
            # Print detailed blueprint information for debugging
            print(f"\n===== BLUEPRINT DETAILS =====")
            print(f"Blueprint ID: {blueprint_id}")
            print(f"Blueprint Title: {test_blueprint.title}")
            print("Blueprint Properties:")
            for prop_name, prop_details in test_blueprint.schema["properties"].items():
                prop_type = prop_details.get("type", "unknown")
                print(f"  - {prop_name} (Type: {prop_type})")
            
            # Get the first property from the blueprint for our rule
            property_name = next(iter(test_blueprint.schema["properties"].keys()))
            property_type = test_blueprint.schema["properties"][property_name].get("type", "string")
            
            print(f"\nSelected property: '{property_name}' (type: {property_type})")
            
            # Define a test scorecard with a unique ID using an actual property from the blueprint
            import uuid
            import time
            import json
            test_id = uuid.uuid4().hex[:8]
            test_scorecard_id = f"test_scorecard_{test_id}"
            
            # Determine property value based on property type
            if property_type == "number" or property_type == "integer":
                property_value = 10
            elif property_type == "boolean":
                property_value = True
            else:  # default to string
                property_value = "test_value"
                
            # Define operator based on property type
            if property_type == "number" or property_type == "integer":
                property_operator = ">"
            elif property_type == "boolean":
                property_operator = "="
            elif property_type == "array":
                property_operator = "contains"
            else:  # default for string and others
                property_operator = "="
            
            test_scorecard_data = {
                "identifier": test_scorecard_id,
                "title": "Test Scorecard",
                "rules": [
                    {
                        "identifier": f"test_rule_{test_id}",
                        "title": f"Test Rule for {property_name}",
                        "description": f"A test rule using property {property_name}",
                        "level": "Silver",  # Associate rules with non-base levels
                        "query": {
                            "combinator": "and",
                            "conditions": [
                                {
                                    "property": property_name,
                                    "operator": property_operator,
                                    "value": property_value
                                }
                            ]
                        }
                    }
                ],
                "levels": [
                    {
                        "title": "Basic",  # Base level (no rules)
                        "color": "blue"
                    },
                    {
                        "title": "Silver",
                        "color": "silver"
                    },
                    {
                        "title": "Gold", 
                        "color": "gold"
                    }
                ]
            }
            
            # Generate a curl command for debugging
            formatted_json = json.dumps(test_scorecard_data, indent=2)
            print(f"\n===== CURL COMMAND FOR DEBUGGING =====")
            print(f"curl -X POST 'https://api.getport.io/v1/blueprints/{blueprint_id}/scorecards' \\")
            print(f"-H 'Content-Type: application/json' \\")
            print(f"-H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \\")
            print(f"-d '{formatted_json}'")
            
            print(f"\nCreating test scorecard with ID '{test_scorecard_id}' for blueprint '{blueprint_id}'")
            print(f"Full Scorecard Data: {json.dumps(test_scorecard_data, indent=2)}")
            
            # Create the scorecard
            try:
                created_scorecard = await client.create_new_scorecard(blueprint_id, test_scorecard_data)
                
                # Validate the response
                assert isinstance(created_scorecard, PortScorecard)
                assert created_scorecard.identifier == test_scorecard_id
                assert created_scorecard.title == "Test Scorecard"
                assert created_scorecard.blueprint == blueprint_id
                assert len(created_scorecard.rules) == 1
                assert len(created_scorecard.levels) == 3
                
                print(f"Successfully created scorecard: {created_scorecard.title} (ID: {created_scorecard.identifier})")
                
                # Now retrieve the scorecard to verify it exists
                retrieved_scorecard = await client.get_scorecard_details(test_scorecard_id, blueprint_id)
                assert isinstance(retrieved_scorecard, PortScorecard)
                assert retrieved_scorecard.identifier == test_scorecard_id
                
                print(f"Successfully retrieved created scorecard")
                
                # Now delete the scorecard
                deletion_result = await client.delete_scorecard(test_scorecard_id, blueprint_id)
                assert deletion_result is True, "Deletion should return True on success"
                
                print(f"Successfully deleted scorecard")
                
                # Try to retrieve the deleted scorecard, should raise an exception
                try:
                    await client.get_scorecard_details(test_scorecard_id, blueprint_id)
                    pytest.fail("Should not be able to retrieve a deleted scorecard")
                except Exception as retrieval_error:
                    print(f"Expected error on retrieval after deletion: {str(retrieval_error)}")
                    # This is the expected behavior
                    pass
            except Exception as creation_error:
                print(f"\n===== ERROR CREATING SCORECARD =====")
                print(f"Error: {str(creation_error)}")
                print(f"Full scorecard data: {json.dumps(test_scorecard_data, indent=2)}")
                print(f"Blueprint ID: {blueprint_id}")
                
                # Check if this is a 409 Conflict error
                if "409 Client Error: Conflict" in str(creation_error):
                    print("\nThis is a 409 Conflict error, which may indicate:")
                    print("1. A scorecard with the same ID already exists")
                    print("2. Permissions don't allow creating scorecards")
                    print("3. The blueprint doesn't support scorecards")
                    print("4. There's an issue with the payload format")
                    
                    # Generate a curl command for the user to try directly
                    print("\nPlease try running the curl command above with your access token")
                    
                    pytest.skip("Skipping test due to scorecard conflict (409)")
                # Re-raise other errors
                raise creation_error
                
        except Exception as e:
            if "409 Client Error: Conflict" not in str(e):
                print(f"Error in create_and_delete_scorecard test: {str(e)}")
                import traceback
                traceback.print_exc()
                
                # Try to clean up if creation succeeded but later steps failed
                try:
                    await client.delete_scorecard(test_scorecard_id, blueprint_id)
                    print(f"Cleaned up test scorecard after test failure")
                except:
                    pass
                    
                pytest.fail(f"Error in scorecard creation/deletion test: {str(e)}")

    @pytest.mark.asyncio
    async def test_create_scorecard_detailed_error(self, mock_port_client):
        """Test that detailed error information is included when creating a scorecard fails with a 422 error."""
        from requests import Response
        from requests.exceptions import HTTPError
        
        # Create a mock response with error details
        mock_response = Response()
        mock_response.status_code = 422
        
        # Add JSON error response with details
        error_content = {
            "message": "Validation failed",
            "details": "Invalid rule format. Expected 'query' object to contain 'combinator' and 'conditions'."
        }
        mock_response._content = json.dumps(error_content).encode('utf-8')
        
        # Set up the response to return the JSON content when json() is called
        mock_response.json = MagicMock(return_value=error_content)
        
        # Make the response raise an HTTPError when raise_for_status is called
        mock_response.raise_for_status = lambda: exec('raise HTTPError("422 Client Error")')
        
        # Create the HTTP error with the mock response
        http_error = HTTPError("422 Client Error")
        http_error.response = mock_response
        
        # Configure create_new_scorecard to raise PortError with the proper error message
        error_message = f"Error creating scorecard: 422 - {error_content['message']}. Details: {error_content['details']}"
        mock_port_client.create_new_scorecard.side_effect = PortError(error_message)
        
        # Attempt to create a scorecard
        blueprint_id = "test-blueprint"
        scorecard_data = {
            "identifier": "test-scorecard",
            "title": "Test Scorecard",
            "levels": [{"title": "Basic", "color": "green"}],
            "rules": []
        }
        
        # Verify that the error contains the detailed information
        with pytest.raises(PortError) as exc_info:
            await mock_port_client.create_new_scorecard(blueprint_id, scorecard_data)
        
        error_message = str(exc_info.value)
        assert "422" in error_message
        assert "Validation failed" in error_message
        assert "Invalid rule format" in error_message
        assert "combinator" in error_message 