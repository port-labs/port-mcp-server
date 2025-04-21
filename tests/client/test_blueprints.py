import os
import pytest
import sys
import json
from dotenv import load_dotenv

# Add the src directory to the path so we can import our modules
sys.path.append('src')

from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.blueprints import PortBlueprintList, PortBlueprint

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
class TestPortBlueprintClient:
    """Tests for the Port Blueprint Client functionality."""

    @pytest.fixture
    def client(self):
        """Create a PortClient instance with credentials."""
        return PortClient(
            client_id=PORT_CLIENT_ID,
            client_secret=PORT_CLIENT_SECRET,
            region=REGION
        )

    @pytest.mark.asyncio
    async def test_get_blueprints(self, client):
        """Test getting all blueprints."""
        # Get all blueprints
        blueprint_list = await client.get_blueprints()
        
        # Create sample data for mocking
        raw_data = []
        for bp in blueprint_list.blueprints:
            raw_bp = {
                "identifier": bp.identifier,
                "title": bp.title,
                "description": bp.description,
                "icon": bp.icon,
                "createdAt": bp.created_at,
                "createdBy": bp.created_by,
                "updatedAt": bp.updated_at,
                "updatedBy": bp.updated_by
            }
            if bp.schema:
                raw_bp["schema"] = bp.schema
            if bp.relations:
                raw_bp["relations"] = bp.relations
            raw_data.append(raw_bp)
        
        # Print the first blueprint's data for mocking
        print("\n===== SAMPLE BLUEPRINT DATA FOR MOCKING =====")
        print(json.dumps(raw_data[0], indent=2))
        print("============================================\n")
        
        # Validate the response
        assert isinstance(blueprint_list, PortBlueprintList)
        assert isinstance(blueprint_list.blueprints, list)
        
        # Print some information for debugging
        print(f"Found {len(blueprint_list.blueprints)} blueprints")
        
        # We should have at least one blueprint
        assert len(blueprint_list.blueprints) > 0
        
        # Validate the first blueprint
        first_blueprint = blueprint_list.blueprints[0]
        assert isinstance(first_blueprint, PortBlueprint)
        assert first_blueprint.identifier
        assert first_blueprint.title
        
        # Print the first blueprint for debugging
        print(f"First blueprint: {first_blueprint.title} (ID: {first_blueprint.identifier})")
        
        # Return the first blueprint ID for use in other tests
        return first_blueprint.identifier
    
    @pytest.mark.asyncio
    async def test_get_blueprint(self, client):
        """Test getting a specific blueprint by identifier."""
        # First get all blueprints to find an ID to use
        blueprint_list = await client.get_blueprints()
        assert len(blueprint_list.blueprints) > 0
        
        # Get the first blueprint's identifier
        blueprint_id = blueprint_list.blueprints[0].identifier
        print(f"Testing get_blueprint with ID: {blueprint_id}")
        
        # Get the specific blueprint
        blueprint = await client.get_blueprint(blueprint_id)
        
        # Create sample data for mocking
        raw_bp = {
            "identifier": blueprint.identifier,
            "title": blueprint.title,
            "description": blueprint.description,
            "icon": blueprint.icon,
            "createdAt": blueprint.created_at,
            "createdBy": blueprint.created_by,
            "updatedAt": blueprint.updated_at,
            "updatedBy": blueprint.updated_by
        }
        if blueprint.schema:
            raw_bp["schema"] = blueprint.schema
        if blueprint.relations:
            raw_bp["relations"] = blueprint.relations
        
        # Print the blueprint data for mocking
        print("\n===== SPECIFIC BLUEPRINT DATA FOR MOCKING =====")
        print(json.dumps(raw_bp, indent=2))
        print("===============================================\n")
        
        # Validate the response
        assert isinstance(blueprint, PortBlueprint)
        assert blueprint.identifier == blueprint_id
        assert blueprint.title
        
        # Check additional properties if they exist
        if blueprint.description:
            assert isinstance(blueprint.description, str)
        
        if blueprint.created_at:
            assert isinstance(blueprint.created_at, str)
            
        if blueprint.updated_at:
            assert isinstance(blueprint.updated_at, str)
        
        # Print blueprint details for debugging
        print(f"Retrieved blueprint: {blueprint.title}")
        print(f"  Description: {blueprint.description}")
        print(f"  Created at: {blueprint.created_at}")
        print(f"  Updated at: {blueprint.updated_at}") 