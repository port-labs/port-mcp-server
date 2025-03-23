import pytest
import sys

# Add the src directory to the path so we can import our modules
sys.path.append('src')

from mcp_server_port.models.models import PortEntityList, PortEntity
from .fixtures.entities import MOCK_ENTITIES_DATA

class TestPortEntityClientMock:
    """Tests for the Port Entity Client functionality using mocks."""

    @pytest.mark.asyncio
    async def test_get_entities_mock(self, mock_client):
        """Test getting all entities for a blueprint with mocked data."""
        # Test for each blueprint type in our mock data
        for blueprint_id, entities in MOCK_ENTITIES_DATA.items():
            print(f"\nTesting get_entities for blueprint: {blueprint_id}")
            
            # Get entities for this blueprint
            entity_list = await mock_client.get_entities(blueprint_id)
            
            # Validate the response
            assert isinstance(entity_list, PortEntityList)
            assert isinstance(entity_list.entities, list)
            assert len(entity_list.entities) == len(entities)
            
            # Validate each entity
            for i, entity in enumerate(entity_list.entities):
                mock_entity = entities[i]
                assert isinstance(entity, PortEntity)
                assert entity.identifier == mock_entity["identifier"]
                assert entity.title == mock_entity["title"]
                assert entity.blueprint == blueprint_id
                assert entity.properties == mock_entity["properties"]
                assert entity.relations == mock_entity["relations"]
                assert entity.created_at == mock_entity["createdAt"]
                assert entity.updated_at == mock_entity["updatedAt"]

    @pytest.mark.asyncio
    async def test_get_entity_mock(self, mock_client):
        """Test getting a specific entity by identifier with mocked data."""
        # Test getting each entity from our mock data
        for blueprint_id, entities in MOCK_ENTITIES_DATA.items():
            for mock_entity in entities:
                entity_id = mock_entity["identifier"]
                print(f"\nTesting get_entity with ID: {entity_id} from blueprint: {blueprint_id}")
                
                # Get the specific entity
                entity = await mock_client.get_entity(blueprint_id, entity_id)
                
                # Validate the response
                assert isinstance(entity, PortEntity)
                assert entity.identifier == entity_id
                assert entity.title == mock_entity["title"]
                assert entity.blueprint == blueprint_id
                assert entity.properties == mock_entity["properties"]
                assert entity.relations == mock_entity["relations"]
                assert entity.created_at == mock_entity["createdAt"]
                assert entity.updated_at == mock_entity["updatedAt"]
                
                # Validate specific properties based on blueprint type
                if blueprint_id == "service":
                    assert "team" in entity.properties
                    assert "healthStatus" in entity.properties
                elif blueprint_id == "deployment":
                    assert "version" in entity.properties
                    assert "environment" in entity.properties
                elif blueprint_id == "component":
                    assert "type" in entity.properties
                    assert "language" in entity.properties 