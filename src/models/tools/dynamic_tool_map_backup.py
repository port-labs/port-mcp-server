from dataclasses import dataclass

from src.client.client import PortClient
from src.models.tools.tool_map import ToolMap
from src.tools.action.dynamic_action_tool_backup import create_dynamic_action_tool
from src.utils import logger


@dataclass
class DynamicToolMap(ToolMap):
    """Extended ToolMap that includes dynamically generated tools from Port actions."""
    
    def __post_init__(self):
        # Initialize with static tools first
        super().__post_init__()
        
        # Then add dynamic action tools
        self._register_dynamic_action_tools()
    
    def _register_dynamic_action_tools(self) -> None:
        """Register dynamic tools for each Port action."""
        try:
            # Use the existing list_actions functionality to get actions
            from src.tools.action.list_actions import ListActionsTool, ListActionsToolSchema
            from src.tools.action.get_action import GetActionTool, GetActionToolSchema
            import asyncio

            # Get all actions
            list_actions_tool = ListActionsTool(self.port_client)
            actions_response = asyncio.run(list_actions_tool.list_actions(ListActionsToolSchema()))
            actions = actions_response.get("actions", [])
            
            # Get detailed action info and create tools
            get_action_tool = GetActionTool(self.port_client)
            dynamic_tools_count = 0
            
            for action_data in actions:
                try:
                    # Handle both dict and ActionSummary objects
                    action_identifier = action_data.get("identifier") if isinstance(action_data, dict) else action_data.identifier
                    
                    # Get full action details
                    action_response = asyncio.run(get_action_tool.get_action(GetActionToolSchema(action_identifier=action_identifier)))
                    from src.models.actions.action import Action
                    action = Action(**action_response)
                    
                    if action:
                        # Create and register dynamic tool
                        dynamic_tool = create_dynamic_action_tool(action, self.port_client)
                        self.register_tool(dynamic_tool)
                        dynamic_tools_count += 1
                        
                except Exception as e:
                    logger.warning(f"Failed to create dynamic tool for action {action_identifier}: {e}")
                    continue
            
            logger.info(f"Registered {dynamic_tools_count} dynamic action tools")
            
        except Exception as e:
            logger.error(f"Failed to register dynamic action tools: {e}") 