import pytest
import sys
import json
from unittest.mock import AsyncMock



from src.server.models import CreateBlueprint
from src.server.tools.blueprint import UpdateBlueprintTool

BLUEPRINT_SCHEMA = {
                'identifier':'updatedBlueprint',
                'title':'Updated Blueprint',
                'schema':{
                    'type':'object',
                    'properties':{   
                        'property_1':{
                            'title':'Property 1',
                            'description':'Property 1 description',
                            'icon':'AWS',
                            'type':'string',
                            'format':'url',
                            'spec':'open-api'
                        },
                        'property_2': {
                            'title':'Property 2',
                            'description':'Property 2 description',
                            'icon':'AWS',
                            'type':'number',
                        },
                },
                'required':['property_1']
                },
            }

@pytest.fixture
def mock_client_for_update(mock_client):
    """Add specific return values for this test"""
    mock_client.update_blueprint.return_value = CreateBlueprint(**BLUEPRINT_SCHEMA)

    return mock_client


@pytest.mark.asyncio
async def test_update_blueprint_tool(mock_client_for_update):
    """Test the UpdateBlueprintTool's metadata and function execution."""
    # Create the tool
    tool = UpdateBlueprintTool(mock_client_for_update)
    
    # Test tool metadata
    assert tool.name == "update_blueprint"
    assert "update" in tool.description.lower()
    assert "blueprint" in tool.description.lower()
    
    
    result = await tool.update_blueprint(tool.validate_input(BLUEPRINT_SCHEMA))
    mock_client_for_update.update_blueprint.assert_awaited_once()
    assert result is not None 