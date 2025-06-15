from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.models.action_run.action_run import ActionRun
from src.models.actions.action import Action, ActionInvocationMethod, ActionTrigger
from src.tools.action.dynamic_actions import (
    DynamicActionToolResponse,
    DynamicActionToolSchema,
    DynamicActionToolsManager,
    _camel_to_snake,
)


class TestCamelToSnake:
    """Test the _camel_to_snake utility function."""

    def test_camel_to_snake_simple(self):
        """Test simple CamelCase conversion."""
        assert _camel_to_snake("CamelCase") == "camel_case"
        assert _camel_to_snake("SimpleTest") == "simple_test"

    def test_camel_to_snake_single_word(self):
        """Test single word conversion."""
        assert _camel_to_snake("test") == "test"
        assert _camel_to_snake("Test") == "test"

    def test_camel_to_snake_with_numbers(self):
        """Test conversion with numbers."""
        assert _camel_to_snake("testAPI2") == "test_api2"
        assert _camel_to_snake("createJiraIssue") == "create_jira_issue"

    def test_camel_to_snake_with_underscores(self):
        """Test conversion with existing underscores."""
        assert _camel_to_snake("test_action") == "test_action"
        assert _camel_to_snake("TestAction_Name") == "test_action__name"

    def test_camel_to_snake_complex_cases(self):
        """Test complex conversion cases."""
        assert _camel_to_snake("XMLHttpRequest") == "xml_http_request"
        assert _camel_to_snake("HTMLParser") == "html_parser"


class TestDynamicActionToolSchema:
    """Test the DynamicActionToolSchema model."""

    def test_schema_creation_empty(self):
        """Test creating schema with no parameters."""
        schema = DynamicActionToolSchema()
        assert schema.entity_identifier is None
        assert schema.properties is None

    def test_schema_creation_with_values(self):
        """Test creating schema with parameters."""
        schema = DynamicActionToolSchema(
            entity_identifier="test-entity", properties={"key": "value", "number": 42}
        )
        assert schema.entity_identifier == "test-entity"
        assert schema.properties == {"key": "value", "number": 42}

    def test_schema_validation(self):
        """Test schema validation."""
        # Valid schema
        schema = DynamicActionToolSchema(
            entity_identifier="valid-entity-123", properties={"test": True}
        )
        assert schema.entity_identifier == "valid-entity-123"
        assert schema.properties == {"test": True}


class TestDynamicActionToolResponse:
    """Test the DynamicActionToolResponse model."""

    def test_response_creation(self):
        """Test creating response with action run."""
        action_run = ActionRun.model_construct(
            id="run-123",
            status="IN_PROGRESS",
            action={"identifier": "test-action", "title": "Test Action"},
            createdAt="2023-12-01T10:00:00Z",
        )

        response = DynamicActionToolResponse(action_run=action_run)
        assert response.action_run.id == "run-123"
        assert response.action_run.status == "IN_PROGRESS"

    def test_response_model_dump(self):
        """Test response model dump."""
        action_run = ActionRun.model_construct(
            id="run-456",
            status="SUCCESS",
            action={"identifier": "test-action", "title": "Test Action"},
            createdAt="2023-12-01T10:00:00Z",
        )

        response = DynamicActionToolResponse(action_run=action_run)
        dumped = response.model_dump()
        assert "action_run" in dumped
        assert dumped["action_run"]["id"] == "run-456"


@pytest.fixture
def mock_action():
    """Create a mock action for testing."""
    return Action.model_construct(
        identifier="createJiraIssue",
        title="Create Jira Issue",
        description="Create a new issue in Jira",
        trigger=ActionTrigger.model_construct(type="self-service", operation="CREATE"),
        invocation_method=ActionInvocationMethod.model_construct(
            type="WEBHOOK", url="https://example.com/webhook"
        ),
    )


@pytest.fixture
def mock_action_run():
    """Create a mock action run for testing."""
    return ActionRun.model_construct(
        id="run-123",
        status="IN_PROGRESS",
        action={"identifier": "createJiraIssue", "title": "Create Jira Issue"},
        createdAt="2023-12-01T10:00:00Z",
    )


@pytest.fixture
def mock_client_for_dynamic_actions(mock_client, mock_action_run):
    """Configure mock client for dynamic action tests."""
    # Set up action_runs attribute
    mock_client.action_runs = mock_client

    # Configure return values
    mock_client.create_global_action_run.return_value = mock_action_run
    mock_client.create_entity_action_run.return_value = mock_action_run

    return mock_client


class TestDynamicActionToolsManager:
    """Test the DynamicActionToolsManager class."""

    def test_manager_initialization(self, mock_client_for_dynamic_actions):
        """Test manager initialization."""
        manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
        assert manager.port_client == mock_client_for_dynamic_actions

    def test_create_dynamic_action_tool(self, mock_client_for_dynamic_actions, mock_action):
        """Test creating a dynamic action tool."""
        manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
        tool = manager._create_dynamic_action_tool(mock_action)

        # Check tool metadata
        assert tool.name == "run_create_jira_issue"
        assert "Create Jira Issue" in tool.description
        assert "Create a new issue in Jira" in tool.description
        assert "createJiraIssue" in tool.description
        assert tool.input_schema == DynamicActionToolSchema
        assert tool.output_schema == DynamicActionToolResponse

    def test_create_dynamic_action_tool_long_name(self, mock_client_for_dynamic_actions):
        """Test creating a dynamic action tool with very long identifier."""
        long_action = Action.model_construct(
            identifier="thisIsAVeryLongActionIdentifierThatExceedsFortyCharacters",
            title="Long Action",
            description="A very long action identifier",
            trigger=ActionTrigger.model_construct(type="self-service"),
            invocation_method=ActionInvocationMethod.model_construct(type="WEBHOOK"),
        )

        manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
        tool = manager._create_dynamic_action_tool(long_action)

        # Name should be truncated to 40 characters
        assert len(tool.name) <= 40
        assert tool.name == "run_this_is_a_very_long_action_identifie"

    def test_create_dynamic_action_tool_no_description(self, mock_client_for_dynamic_actions):
        """Test creating a dynamic action tool without description."""
        action_no_desc = Action.model_construct(
            identifier="simpleAction",
            title="Simple Action",
            description=None,
            trigger=ActionTrigger.model_construct(type="self-service"),
            invocation_method=ActionInvocationMethod.model_construct(type="WEBHOOK"),
        )

        manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
        tool = manager._create_dynamic_action_tool(action_no_desc)

        # Description should not contain action description
        assert "Execute the 'Simple Action' action" in tool.description
        assert "To see required properties" in tool.description

    @pytest.mark.asyncio
    async def test_dynamic_action_function_global(
        self, mock_client_for_dynamic_actions, mock_action, mock_action_run
    ):
        """Test the dynamic action function for global actions."""
        manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
        tool = manager._create_dynamic_action_tool(mock_action)

        # Test global action execution
        schema = DynamicActionToolSchema(
            entity_identifier=None, properties={"summary": "Test issue", "priority": "High"}
        )

        result = await tool.function(schema)

        # Verify client was called correctly
        mock_client_for_dynamic_actions.create_global_action_run.assert_awaited_once_with(
            action_identifier="createJiraIssue",
            properties={"summary": "Test issue", "priority": "High"},
        )

        # Verify result
        assert "action_run" in result
        assert result["action_run"]["id"] == "run-123"

    @pytest.mark.asyncio
    async def test_dynamic_action_function_entity(
        self, mock_client_for_dynamic_actions, mock_action, mock_action_run
    ):
        """Test the dynamic action function for entity-specific actions."""
        manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
        tool = manager._create_dynamic_action_tool(mock_action)

        # Test entity action execution
        schema = DynamicActionToolSchema(
            entity_identifier="test-entity-123", properties={"summary": "Entity issue"}
        )

        result = await tool.function(schema)

        # Verify client was called correctly
        mock_client_for_dynamic_actions.create_entity_action_run.assert_awaited_once_with(
            action_identifier="createJiraIssue",
            entity="test-entity-123",
            properties={"summary": "Entity issue"},
        )

        # Verify result
        assert "action_run" in result
        assert result["action_run"]["id"] == "run-123"

    @pytest.mark.asyncio
    async def test_dynamic_action_function_no_properties(
        self, mock_client_for_dynamic_actions, mock_action
    ):
        """Test the dynamic action function with no properties."""
        manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
        tool = manager._create_dynamic_action_tool(mock_action)

        # Test with no properties
        schema = DynamicActionToolSchema()

        await tool.function(schema)

        # Verify empty properties dict was passed
        mock_client_for_dynamic_actions.create_global_action_run.assert_awaited_once_with(
            action_identifier="createJiraIssue", properties={}
        )

    @pytest.mark.asyncio
    async def test_dynamic_action_function_no_action_runs(
        self, mock_client_for_dynamic_actions, mock_action
    ):
        """Test the dynamic action function when action_runs is not available."""
        # Remove action_runs from client
        mock_client_for_dynamic_actions.action_runs = None

        manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
        tool = manager._create_dynamic_action_tool(mock_action)

        schema = DynamicActionToolSchema()

        with pytest.raises(ValueError, match="Action runs client not available"):
            await tool.function(schema)

    @pytest.mark.asyncio
    async def test_get_dynamic_action_tools_success(self, mock_client_for_dynamic_actions):
        """Test successful creation of dynamic action tools."""
        # Mock the list_actions and get_action tools
        mock_actions_response = {
            "actions": [
                {"identifier": "action1", "title": "Action 1"},
                {"identifier": "action2", "title": "Action 2"},
            ]
        }

        mock_action_1 = Action.model_construct(
            identifier="action1",
            title="Action 1",
            trigger=ActionTrigger.model_construct(type="self-service"),
            invocation_method=ActionInvocationMethod.model_construct(type="WEBHOOK"),
        )

        mock_action_2 = Action.model_construct(
            identifier="action2",
            title="Action 2",
            trigger=ActionTrigger.model_construct(type="self-service"),
            invocation_method=ActionInvocationMethod.model_construct(type="WEBHOOK"),
        )

        with patch(
            "src.tools.action.dynamic_actions.ListActionsTool"
        ) as mock_list_tool_class, patch(
            "src.tools.action.dynamic_actions.GetActionTool"
        ) as mock_get_tool_class:
            # Configure mock list tool
            mock_list_tool = MagicMock()
            mock_list_tool.list_actions = AsyncMock(return_value=mock_actions_response)
            mock_list_tool_class.return_value = mock_list_tool

            # Configure mock get tool
            mock_get_tool = MagicMock()
            mock_get_tool.get_action = AsyncMock()
            mock_get_tool.get_action.side_effect = [
                mock_action_1.model_dump(),
                mock_action_2.model_dump(),
            ]
            mock_get_tool_class.return_value = mock_get_tool

            manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
            tools = await manager.get_dynamic_action_tools()

            # Verify results
            assert len(tools) == 2
            assert tools[0].name == "run_action1"
            assert tools[1].name == "run_action2"
            assert "Action 1" in tools[0].description
            assert "Action 2" in tools[1].description

    @pytest.mark.asyncio
    async def test_get_dynamic_action_tools_with_object_actions(
        self, mock_client_for_dynamic_actions
    ):
        """Test handling of action objects vs dictionaries."""
        # Mock actions as objects instead of dictionaries
        mock_action_obj = Action.model_construct(
            identifier="objectAction",
            title="Object Action",
            trigger=ActionTrigger.model_construct(type="self-service"),
            invocation_method=ActionInvocationMethod.model_construct(type="WEBHOOK"),
        )

        mock_actions_response = {"actions": [mock_action_obj]}  # Action object instead of dict

        with patch(
            "src.tools.action.dynamic_actions.ListActionsTool"
        ) as mock_list_tool_class, patch(
            "src.tools.action.dynamic_actions.GetActionTool"
        ) as mock_get_tool_class:
            mock_list_tool = MagicMock()
            mock_list_tool.list_actions = AsyncMock(return_value=mock_actions_response)
            mock_list_tool_class.return_value = mock_list_tool

            mock_get_tool = MagicMock()
            mock_get_tool.get_action = AsyncMock(return_value=mock_action_obj.model_dump())
            mock_get_tool_class.return_value = mock_get_tool

            manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
            tools = await manager.get_dynamic_action_tools()

            assert len(tools) == 1
            assert tools[0].name == "run_object_action"

    @pytest.mark.asyncio
    async def test_get_dynamic_action_tools_skip_no_identifier(
        self, mock_client_for_dynamic_actions
    ):
        """Test skipping actions without identifiers."""
        mock_actions_response = {
            "actions": [
                {"identifier": "validAction", "title": "Valid Action"},
                {"title": "Invalid Action"},  # No identifier
                {"identifier": None, "title": "Null Identifier"},  # Null identifier
            ]
        }

        mock_action = Action.model_construct(
            identifier="validAction",
            title="Valid Action",
            trigger=ActionTrigger.model_construct(type="self-service"),
            invocation_method=ActionInvocationMethod.model_construct(type="WEBHOOK"),
        )

        with patch(
            "src.tools.action.dynamic_actions.ListActionsTool"
        ) as mock_list_tool_class, patch(
            "src.tools.action.dynamic_actions.GetActionTool"
        ) as mock_get_tool_class:
            mock_list_tool = MagicMock()
            mock_list_tool.list_actions = AsyncMock(return_value=mock_actions_response)
            mock_list_tool_class.return_value = mock_list_tool

            mock_get_tool = MagicMock()
            mock_get_tool.get_action = AsyncMock(return_value=mock_action.model_dump())
            mock_get_tool_class.return_value = mock_get_tool

            manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
            tools = await manager.get_dynamic_action_tools()

            # Should only create tool for the valid action
            assert len(tools) == 1
            assert tools[0].name == "run_valid_action"

    @pytest.mark.asyncio
    async def test_get_dynamic_action_tools_handle_individual_failures(
        self, mock_client_for_dynamic_actions
    ):
        """Test handling individual action failures gracefully."""
        mock_actions_response = {
            "actions": [
                {"identifier": "goodAction", "title": "Good Action"},
                {"identifier": "badAction", "title": "Bad Action"},
            ]
        }

        mock_good_action = Action.model_construct(
            identifier="goodAction",
            title="Good Action",
            trigger=ActionTrigger.model_construct(type="self-service"),
            invocation_method=ActionInvocationMethod.model_construct(type="WEBHOOK"),
        )

        with patch(
            "src.tools.action.dynamic_actions.ListActionsTool"
        ) as mock_list_tool_class, patch(
            "src.tools.action.dynamic_actions.GetActionTool"
        ) as mock_get_tool_class:
            mock_list_tool = MagicMock()
            mock_list_tool.list_actions = AsyncMock(return_value=mock_actions_response)
            mock_list_tool_class.return_value = mock_list_tool

            mock_get_tool = MagicMock()
            # First call succeeds, second fails
            mock_get_tool.get_action = AsyncMock()
            mock_get_tool.get_action.side_effect = [
                mock_good_action.model_dump(),
                Exception("Failed to get action"),
            ]
            mock_get_tool_class.return_value = mock_get_tool

            manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
            tools = await manager.get_dynamic_action_tools()

            # Should only create tool for the successful action
            assert len(tools) == 1
            assert tools[0].name == "run_good_action"

    @pytest.mark.asyncio
    async def test_get_dynamic_action_tools_complete_failure(self, mock_client_for_dynamic_actions):
        """Test handling complete failure in getting dynamic tools."""
        with patch("src.tools.action.dynamic_actions.ListActionsTool") as mock_list_tool_class:
            mock_list_tool = MagicMock()
            mock_list_tool.list_actions = AsyncMock(side_effect=Exception("API failure"))
            mock_list_tool_class.return_value = mock_list_tool

            manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)
            tools = await manager.get_dynamic_action_tools()

            # Should return empty list on complete failure
            assert tools == []

    def test_get_dynamic_action_tools_sync(self, mock_client_for_dynamic_actions):
        """Test the synchronous wrapper for getting dynamic tools."""
        with patch.object(
            DynamicActionToolsManager, "get_dynamic_action_tools"
        ) as mock_async_method:
            mock_async_method.return_value = []

            manager = DynamicActionToolsManager(mock_client_for_dynamic_actions)

            # Mock asyncio.run to avoid actual async execution in test
            with patch("asyncio.run") as mock_run:
                mock_run.return_value = []

                result = manager.get_dynamic_action_tools_sync()

                mock_run.assert_called_once()
                assert result == []
