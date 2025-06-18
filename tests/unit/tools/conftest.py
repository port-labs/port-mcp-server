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
    client.search_entities = AsyncMock()
    client.create_entity = AsyncMock()
    client.update_entity = AsyncMock()
    client.delete_entity = AsyncMock()

    client.get_scorecard = AsyncMock()
    client.get_scorecards = AsyncMock()
    client.create_scorecard = AsyncMock()
    client.update_scorecard = AsyncMock()
    client.delete_scorecard = AsyncMock()

    client.get_action = AsyncMock()
    client.get_all_actions = AsyncMock()
    client.create_action = AsyncMock()
    client.update_action = AsyncMock()
    client.delete_action = AsyncMock()
    client.create_global_action_run = AsyncMock()
    client.create_blueprint_action_run = AsyncMock()
    client.create_entity_action_run = AsyncMock()
    client.get_action_run = AsyncMock()

    client.trigger_agent = AsyncMock()
    client.get_invocation_status = AsyncMock()

    # Add action_runs mock for dynamic actions
    client.action_runs = MagicMock()

    return client


@pytest.fixture
def mock_client_for_dynamic_actions(mock_client):
    """Mock client specifically for dynamic actions tests."""
    from src.models.action_run.action_run import ActionRun
    
    # Mock action run return value
    mock_action_run = ActionRun.model_construct(
        id="run-123",
        status="IN_PROGRESS",
        action={"identifier": "createJiraIssue", "title": "Create Jira Issue"},
        createdAt="2023-12-01T10:00:00Z",
    )
    
    mock_client.create_global_action_run.return_value = mock_action_run
    mock_client.create_blueprint_action_run.return_value = mock_action_run
    mock_client.create_entity_action_run.return_value = mock_action_run
    
    return mock_client
