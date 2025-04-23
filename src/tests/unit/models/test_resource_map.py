import pytest
from unittest.mock import MagicMock
from .conftest import TestBaseResource, Resource, clean_resource_map

@pytest.mark.asyncio
async def test_resource_map_registration_and_lookup(clean_resource_map):
    """Test that ResourceMap correctly registers and looks up resources."""
    # Use the clean resource map from the fixture
    resource_map = clean_resource_map
    
    # Create a test resource
    resource = TestBaseResource()
    
    # Register the resource
    resource_map.register_resource(resource)
    
    # Look up the resource
    found_resource = resource_map.get_resource("test_resource")
    
    # Verify the resource
    assert found_resource is resource
    
    # Verify looking up a non-existent resource raises an error
    with pytest.raises(ValueError) as excinfo:
        resource_map.get_resource("non_existent_resource")
    
    # Verify the error
    assert "Resource not found" in str(excinfo.value)
    
    # Verify listing resources
    resources = resource_map.list_resources()
    assert len(resources) == 1
    assert resources[0].name == "test_resource"
    assert resources[0].description == "A resource for testing"
    assert str(resources[0].uri) == "test://{param}"
    assert resources[0].mimeType == "text/plain"


@pytest.mark.asyncio
async def test_resource_map_error_handling(clean_resource_map):
    """Test error handling in ResourceMap."""
    # Use the clean resource map from the fixture
    resource_map = clean_resource_map
    
    # Create a mock resource with missing required attributes
    invalid_resource = MagicMock(spec=Resource)
    invalid_resource.name = None
    invalid_resource.uri = "invalid://resource"
    
    with pytest.raises(ValueError) as excinfo:
        resource_map.register_resource(invalid_resource)
    assert "Resource must have a name" in str(excinfo.value)
    
    # Test registering a resource with a duplicate name
    # First create and register a valid resource
    resource1 = TestBaseResource()
    resource_map.register_resource(resource1)
    
    # Then try to register another resource with the same name
    resource2 = MagicMock(spec=Resource)
    resource2.name = "test_resource"  # Same name as resource1
    resource2.uri = "test://duplicate"
    
    with pytest.raises(ValueError) as excinfo:
        resource_map.register_resource(resource2)
    assert "Resource with name 'test_resource' already registered" in str(excinfo.value) 