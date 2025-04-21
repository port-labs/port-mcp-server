import pytest
import sys

# Add the src directory to the path so we can import our modules
sys.path.append('src')

from src.mcp_server_port.models.blueprints import PortBlueprintList, PortBlueprint
from .conftest import MOCK_BLUEPRINTS_DATA

class TestPortBlueprintClientMock:
    """Tests for the Port Blueprint Client functionality using mocks."""

    @pytest.mark.asyncio
    async def test_get_blueprints_mock(self, mock_client):
        """Test getting all blueprints with mocked data."""
        # Get all blueprints
        blueprint_list = await mock_client.get_blueprints()
        
        # Validate the response
        assert isinstance(blueprint_list, PortBlueprintList)
        assert isinstance(blueprint_list.blueprints, list)
        
        # We should have the same number of blueprints as our mock data
        assert len(blueprint_list.blueprints) == len(MOCK_BLUEPRINTS_DATA)
        print(f"Found {len(blueprint_list.blueprints)} blueprints")
        
        # Validate the first blueprint
        first_blueprint = blueprint_list.blueprints[0]
        assert isinstance(first_blueprint, PortBlueprint)
        assert first_blueprint.identifier == MOCK_BLUEPRINTS_DATA[0]["identifier"]
        assert first_blueprint.title == MOCK_BLUEPRINTS_DATA[0]["title"]
        
        # Print the first blueprint for debugging
        print(f"First blueprint: {first_blueprint.title} (ID: {first_blueprint.identifier})")
        
        # Also check that we can find the other blueprints by their identifiers
        blueprint_ids = [bp.identifier for bp in blueprint_list.blueprints]
        assert "service" in blueprint_ids
        assert "deployment" in blueprint_ids
        assert "component" in blueprint_ids

    @pytest.mark.asyncio
    async def test_get_blueprint_mock(self, mock_client):
        """Test getting a specific blueprint by identifier with mocked data."""
        # Test for each blueprint in our mock data
        for mock_blueprint in MOCK_BLUEPRINTS_DATA:
            blueprint_id = mock_blueprint["identifier"]
            print(f"\nTesting get_blueprint with ID: {blueprint_id}")
            
            # Get the specific blueprint
            blueprint = await mock_client.get_blueprint(blueprint_id)
            
            # Validate the response
            assert isinstance(blueprint, PortBlueprint)
            assert blueprint.identifier == blueprint_id
            assert blueprint.title == mock_blueprint["title"]
            assert blueprint.description == mock_blueprint["description"]
            
            # Validate other properties
            assert blueprint.created_at == mock_blueprint["createdAt"]
            assert blueprint.updated_at == mock_blueprint["updatedAt"]
            
            # Print blueprint details for debugging
            print(f"Retrieved blueprint: {blueprint.title}")
            print(f"  Description: {blueprint.description}")
            
            # Check for relations if they exist
            if "relations" in mock_blueprint:
                print("  Relations:")
                for rel_name, rel_info in mock_blueprint["relations"].items():
                    print(f"    - {rel_name}: targets {rel_info['target']}, " +
                          f"required: {rel_info['required']}, many: {rel_info['many']}")
                assert blueprint.relations is not None
                
            # Check for schema if it exists
            if "schema" in mock_blueprint and "properties" in mock_blueprint["schema"]:
                print("  Properties:")
                for prop_name in mock_blueprint["schema"]["properties"].keys():
                    print(f"    - {prop_name}")
                assert blueprint.schema is not None 