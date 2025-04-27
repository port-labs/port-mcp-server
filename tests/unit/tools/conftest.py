from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_client():
    """Create a mock client with common methods."""
    client = MagicMock()

    # Common client methods for all tools
    client.get_blueprints = AsyncMock()
    client.get_blueprint = AsyncMock()
    client.create_blueprint = AsyncMock()
    client.update_blueprint = AsyncMock()
    client.delete_blueprint = AsyncMock()

    client.get_entity = AsyncMock()
    client.get_entities = AsyncMock()
    client.create_entity = AsyncMock()
    client.update_entity = AsyncMock()
    client.delete_entity = AsyncMock()

    client.get_scorecard = AsyncMock()
    client.get_scorecards = AsyncMock()
    client.create_scorecard = AsyncMock()
    client.update_scorecard = AsyncMock()
    client.delete_scorecard = AsyncMock()

    client.trigger_agent = AsyncMock()
    client.get_invocation_status = AsyncMock()

    return client
