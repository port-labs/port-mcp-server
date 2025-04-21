"""Client fixtures for Port client tests."""

import pytest
from unittest.mock import MagicMock, patch

from src.mcp_server_port.client import PortClient
from .blueprints import MOCK_BLUEPRINTS_DATA
from .entities import MOCK_ENTITIES_DATA
from .scorecards import MOCK_SCORECARDS_DATA, MOCK_SCORECARD_DICT

@pytest.fixture
def mock_client():
    """Create a mocked PortClient instance."""
    with patch('pyport.PortClient') as mock_port_client:
        # Create a mock for the underlying SDK client
        sdk_client_mock = MagicMock()
        
        # Set up the blueprints property on the SDK client mock
        sdk_client_mock.blueprints = MagicMock()
        sdk_client_mock.entities = MagicMock()
        sdk_client_mock.scorecards = MagicMock()
        
        # Set up the blueprints methods
        sdk_client_mock.blueprints.get_blueprints = MagicMock(return_value=MOCK_BLUEPRINTS_DATA)
        
        def mock_get_blueprint(blueprint_id):
            for bp in MOCK_BLUEPRINTS_DATA:
                if bp["identifier"] == blueprint_id:
                    return bp
            raise Exception(f"Blueprint with ID {blueprint_id} not found")
            
        sdk_client_mock.blueprints.get_blueprint = MagicMock(side_effect=mock_get_blueprint)
        
        # Set up the entities methods
        def mock_get_entities(blueprint_id):
            if blueprint_id in MOCK_ENTITIES_DATA:
                return MOCK_ENTITIES_DATA[blueprint_id]
            return []
            
        def mock_get_entity(blueprint_id, entity_id):
            if blueprint_id in MOCK_ENTITIES_DATA:
                for entity in MOCK_ENTITIES_DATA[blueprint_id]:
                    if entity["identifier"] == entity_id:
                        return entity
            raise Exception(f"Entity with ID {entity_id} not found in blueprint {blueprint_id}")
            
        sdk_client_mock.entities.get_entities = MagicMock(side_effect=mock_get_entities)
        sdk_client_mock.entities.get_entity = MagicMock(side_effect=mock_get_entity)
        
        # Set up the scorecard methods
        def mock_get_scorecards():
            return MOCK_SCORECARDS_DATA
            
        def mock_get_scorecard(scorecard_id):
            if scorecard_id in MOCK_SCORECARD_DICT:
                # In a real API, this would probably be wrapped in a 'scorecard' key
                return {"scorecard": MOCK_SCORECARD_DICT[scorecard_id]}
            raise Exception(f"Scorecard with ID {scorecard_id} not found")
            
        def mock_create_scorecard(blueprint_id, scorecard_data):
            return {"scorecard": scorecard_data}
            
        # Add scorecard methods
        sdk_client_mock.scorecards.get_scorecards = MagicMock(side_effect=mock_get_scorecards)
        sdk_client_mock.scorecards.get_scorecard = MagicMock(side_effect=mock_get_scorecard)
        sdk_client_mock.scorecards.create_scorecard = MagicMock(side_effect=mock_create_scorecard)
        
        # Mock the make_request method for direct API calls
        def mock_make_request(method, path, **kwargs):
            mock_response = MagicMock()
            mock_response.status_code = 200  # Default to 200 OK
            
            if path == "scorecards":
                # Mock response for GET /scorecards
                mock_response.json.return_value = {"ok": True, "scorecards": MOCK_SCORECARDS_DATA}
            elif path.startswith("blueprints/") and "/scorecards/" in path:
                # Mock response for GET /blueprints/{blueprint_id}/scorecards/{scorecard_id}
                parts = path.split("/")
                if len(parts) >= 4:
                    blueprint_id = parts[1]
                    scorecard_id = parts[3]
                    
                    # Find the matching scorecard
                    for scorecard in MOCK_SCORECARDS_DATA:
                        if scorecard["identifier"] == scorecard_id and scorecard["blueprint"] == blueprint_id:
                            if method == "GET":
                                mock_response.json.return_value = {"ok": True, "scorecard": scorecard}
                            elif method == "DELETE":
                                # For DELETE, just return a successful status code
                                mock_response.status_code = 204
                                # Ensure json doesn't return anything for 204 No Content response
                                mock_response.json.side_effect = Exception("No content in DELETE response")
                            break
                    else:
                        if method == "GET":
                            mock_response.status_code = 404
                            mock_response.json.return_value = {"ok": False, "error": f"Scorecard {scorecard_id} not found in blueprint {blueprint_id}"}
                        elif method == "DELETE":
                            mock_response.status_code = 404
                            mock_response.json.return_value = {"ok": False, "error": f"Cannot delete: Scorecard {scorecard_id} not found in blueprint {blueprint_id}"}
            elif path.startswith("blueprints/") and path.endswith("/scorecards") and method == "POST":
                # Mock response for POST /blueprints/{blueprint_id}/scorecards
                mock_response.status_code = 201
                mock_response.json.return_value = {"ok": True, "scorecard": kwargs.get("json", {})}
            
            return mock_response
            
        sdk_client_mock.make_request = MagicMock(side_effect=mock_make_request)
        
        # Mock returns the SDK client mock
        mock_port_client.return_value = sdk_client_mock
        
        # Create a real PortClient but with a mocked SDK client
        client = PortClient(client_id="mock_id", client_secret="mock_secret")
        
        yield client 