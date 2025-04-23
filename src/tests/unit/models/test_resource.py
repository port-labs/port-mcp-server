import pytest
from .conftest import TestBaseResource

@pytest.mark.asyncio
async def test_base_resource_call():
    """Test that BaseResource.__call__ correctly returns resource content."""
    # Create a test resource
    resource = TestBaseResource()
    
    # Call the resource
    result = await resource()
    
    # Verify the result
    assert result == "Resource content for default"
    
    # Call with parameter
    result = await resource(param="test")
    
    # Verify the result
    assert result == "Resource content for test"


def test_resource_attributes():
    """Test that Resource correctly initializes with all required attributes."""
    resource = TestBaseResource()
    
    # Verify attributes
    assert resource.name == "test_resource"
    assert resource.description == "A resource for testing"
    assert resource.uri == "test://{param}"
    assert resource.mimeType == "text/plain"
    assert callable(resource.function) 