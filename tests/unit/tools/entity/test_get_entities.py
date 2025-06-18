import pytest

from src.models import EntityResult
from src.tools.entity import GetEntitiesTool


@pytest.fixture
def mock_client_with_entities(mock_client):
    """Add specific return values for this test"""
    mock_client.search_entities.return_value = [EntityResult(identifier="test-entity", blueprint="test-blueprint")]
    return mock_client


@pytest.mark.asyncio
async def test_get_entities_tool_detailed_true(mock_client_with_entities):
    """Test the GetEntitiesTool's metadata and function execution with detailed=True."""
    tool = GetEntitiesTool(mock_client_with_entities)

    assert tool.name == "get_entities"
    assert "entities" in tool.description.lower()

    schema = {"blueprint_identifier": "test-blueprint", "detailed": True}
    result = await tool.get_entities(tool.validate_input(schema))
    
    # Verify search_entities was called with correct query (no include filter for detailed=True)
    expected_query = {"query": {"$blueprint": {"=": "test-blueprint"}}}
    mock_client_with_entities.search_entities.assert_awaited_once_with("test-blueprint", expected_query)
    assert result is not None


@pytest.mark.asyncio
async def test_get_entities_tool_detailed_false(mock_client_with_entities):
    """Test the GetEntitiesTool's function execution with detailed=False."""
    tool = GetEntitiesTool(mock_client_with_entities)

    schema = {"blueprint_identifier": "test-blueprint", "detailed": False}
    result = await tool.get_entities(tool.validate_input(schema))
    
    # Verify search_entities was called with correct query (include filter for detailed=False)
    expected_query = {
        "query": {"$blueprint": {"=": "test-blueprint"}},
        "include": ["$identifier", "$title"]
    }
    mock_client_with_entities.search_entities.assert_awaited_once_with("test-blueprint", expected_query)
    assert result is not None


@pytest.mark.asyncio
async def test_get_entities_tool_default_detailed(mock_client_with_entities):
    """Test the GetEntitiesTool's function execution with default detailed value."""
    tool = GetEntitiesTool(mock_client_with_entities)

    schema = {"blueprint_identifier": "test-blueprint"}
    result = await tool.get_entities(tool.validate_input(schema))
    
    # Verify search_entities was called with correct query (include filter for default detailed=False)
    expected_query = {
        "query": {"$blueprint": {"=": "test-blueprint"}},
        "include": ["$identifier", "$title"]
    }
    mock_client_with_entities.search_entities.assert_awaited_once_with("test-blueprint", expected_query)
    assert result is not None
