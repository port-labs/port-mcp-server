"""Client fixtures for Port client tests."""

import pytest
from unittest.mock import MagicMock, patch

from mcp_server_port.client import PortClient
from .blueprints import MOCK_BLUEPRINTS_DATA
from .entities import MOCK_ENTITIES_DATA

@pytest.fixture
def mock_client():
    """Create a mocked PortClient instance."""
    with patch('pyport.PortClient') as mock_port_client:
        # Create a mock for the underlying SDK client
        sdk_client_mock = MagicMock()
        
        # Set up the blueprints property on the SDK client mock
        sdk_client_mock.blueprints = MagicMock()
        sdk_client_mock.entities = MagicMock()
        
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
        
        # Mock returns the SDK client mock
        mock_port_client.return_value = sdk_client_mock
        
        # Create a real PortClient but with a mocked SDK client
        client = PortClient(client_id="mock_id", client_secret="mock_secret")
        
        yield client 