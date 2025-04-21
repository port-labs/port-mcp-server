import os
import pytest
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import our modules
sys.path.append('src')

from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.entities import PortEntityList, PortEntity

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
class TestPortEntityClient:
    """Tests for the Port Entity Client functionality."""

    @pytest.fixture
    def client(self):
        """Create a PortClient instance with credentials."""
        return PortClient(
            client_id=PORT_CLIENT_ID,
            client_secret=PORT_CLIENT_SECRET,
            region=REGION
        )

    @pytest.mark.asyncio
    async def test_entity_operations(self, client):
        """Test a sequence of entity operations:
        1. Get blueprints and choose one
        2. Get entities for that blueprint
        3. Get a specific entity by ID
        """
        # Step 1: Get all blueprints and choose one
        blueprint_list = await client.get_blueprints()
        assert len(blueprint_list.blueprints) > 0
        blueprint = blueprint_list.blueprints[0]
        print(f"Testing with blueprint: {blueprint.identifier}")

        # Step 2: Get entities for the selected blueprint
        entity_list = await client.get_entities(blueprint.identifier)
        assert len(entity_list.entities) > 0
        print(f"Found {len(entity_list.entities)} entities")
        
        # Step 3: Get a specific entity
        selected_entity = entity_list.entities[0]
        entity = await client.get_entity(blueprint.identifier, selected_entity.identifier)
        print(f"Retrieved entity: {entity.identifier}")
        
        # Validate the entity
        assert isinstance(entity, PortEntity)
        assert entity.identifier == selected_entity.identifier
        assert entity.blueprint == blueprint.identifier
        assert entity.properties is not None
        assert entity.relations is not None 