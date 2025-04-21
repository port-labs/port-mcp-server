import pytest
import sys
from unittest.mock import AsyncMock, MagicMock, patch

# Add src to path
sys.path.append('src')

from src.mcp_server_port.models.resources.resource_map import ResourceMap
from src.mcp_server_port.models.resources.base_resource import BaseResource
from src.mcp_server_port.resources.blueprint.get_blueprint import GetBlueprints


class MockResource(BaseResource):
    """Mock resource for testing."""
    name = "mock_resource"
    description = "A mock resource for testing"
    uri = "mock://{param}"
    mime_type = "text/plain"
    
    async def __call__(self, param="default"):
        return f"Resource called with {param}"


@pytest.fixture
def mock_client():
    """Create a mock client."""
    client = MagicMock()
    client.blueprints = AsyncMock()
    client.blueprints.get_blueprints.return_value = [{"id": "test-blueprint"}]
    client.blueprints.get_blueprint.return_value = {"id": "test-blueprint", "properties": {}}
    return client


@pytest.fixture
def resource_map():
    """Create a ResourceMap instance."""
    return ResourceMap()


def test_resource_map_registration(resource_map):
    """Test that resources can be registered with the ResourceMap."""
    mock_resource = MockResource(None)
    resource_map.register_resource(mock_resource)
    
    assert "mock_resource" in resource_map.resources
    assert resource_map.resources["mock_resource"] is mock_resource
    
    # Test getting resource
    assert resource_map.get_resource("mock_resource") is mock_resource
    
    # Test getting non-existent resource
    with pytest.raises(ValueError):
        resource_map.get_resource("non_existent_resource")
    
    # Test listing resources
    resources_list = resource_map.list_resources()
    assert len(resources_list) == 1
    assert resources_list[0]["name"] == "mock_resource"
    assert resources_list[0]["description"] == "A mock resource for testing"
    assert resources_list[0]["uri"] == "mock://{param}"
    assert resources_list[0]["mimeType"] == "text/plain"


@pytest.mark.asyncio
async def test_get_blueprints_resource(mock_client):
    """Test the GetBlueprints resource."""
    # Create the resource
    resource = GetBlueprints(mock_client)
    
    # Test resource metadata
    assert resource.name == "get_blueprints"
    assert "blueprint" in resource.description.lower()
    assert resource.uri == "blueprints://{blueprint_id}"
    assert resource.mime_type == "application/json"
    
    # Test calling resource with no parameters (get all blueprints)
    result = await resource()
    mock_client.blueprints.get_blueprints.assert_awaited_once()
    assert isinstance(result, str)  # Result should be a JSON string
    
    # Reset mock
    mock_client.blueprints.get_blueprints.reset_mock()
    
    # Test calling resource with a blueprint ID
    result = await resource(blueprint_id="test-blueprint")
    mock_client.blueprints.get_blueprint.assert_awaited_once_with("test-blueprint")
    assert isinstance(result, str)  # Result should be a JSON string


@pytest.mark.asyncio
async def test_resource_map_get_resource_callable(resource_map):
    """Test that get_resource returns a callable function."""
    mock_resource = MockResource(None)
    resource_map.register_resource(mock_resource)
    
    # Get the resource function
    resource_fn = resource_map.get_resource("mock_resource")
    
    # Ensure it's callable
    assert callable(resource_fn)
    
    # Call the resource function
    result = await resource_fn()
    assert result == "Resource called with default"
    
    # Call with parameter
    result = await resource_fn(param="test")
    assert result == "Resource called with test" 