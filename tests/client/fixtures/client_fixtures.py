"""Client fixtures for Port client tests."""

import pytest
from unittest.mock import MagicMock, patch

from mcp_server_port.client import PortClient
from .blueprints import MOCK_BLUEPRINTS_DATA

@pytest.fixture
def mock_client():
    """Create a mocked PortClient instance."""
    with patch('pyport.PortClient') as mock_port_client:
        # Create a mock for the underlying SDK client
        sdk_client_mock = MagicMock()
        
        # Set up the blueprints property on the SDK client mock
        sdk_client_mock.blueprints = MagicMock()
        
        # Set up the get_blueprints method on the blueprints property
        sdk_client_mock.blueprints.get_blueprints = MagicMock(return_value=MOCK_BLUEPRINTS_DATA)
        
        # Set up the get_blueprint method to return a specific blueprint by ID
        def mock_get_blueprint(blueprint_id):
            for bp in MOCK_BLUEPRINTS_DATA:
                if bp["identifier"] == blueprint_id:
                    return bp
            raise Exception(f"Blueprint with ID {blueprint_id} not found")
            
        sdk_client_mock.blueprints.get_blueprint = MagicMock(side_effect=mock_get_blueprint)
        
        # Mock returns the SDK client mock
        mock_port_client.return_value = sdk_client_mock
        
        # Create a real PortClient but with a mocked SDK client
        client = PortClient(client_id="mock_id", client_secret="mock_secret")
        
        yield client 