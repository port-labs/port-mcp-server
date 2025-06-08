import re
from typing import Any

from pyport import PortClient

from src.config import config
from src.models.agent.port_agent_response import PortAgentResponse, PortAgentTriggerResponse
from src.utils import logger
from src.utils.errors import PortError


class PortAgentClient:
    _client: PortClient

    def __init__(self, client: PortClient):
        self._client = client

    async def trigger_agent(self, prompt: str) -> PortAgentTriggerResponse:
        endpoint = "agent/invoke"
        data = {"prompt": prompt}

        response = self._client.make_request(method="POST", endpoint=endpoint, json=data)

        response_data: dict[str, Any] = response.json()

        if not response_data.get("ok") or not response_data.get("invocation", {}).get("identifier"):
            logger.error("Response missing required invocation identifier")
            logger.error(f"Response data: {response_data}")
            raise PortError("Response missing required invocation identifier")

        try:
            return PortAgentTriggerResponse(**response_data)
        except Exception as e:
            logger.error(f"Failed to parse trigger agent response: {e}")
            logger.error(f"Response data: {response_data}")
            raise PortError(f"Invalid response format: {response_data}") from e

    async def get_invocation_status(self, identifier: str) -> PortAgentResponse:
        endpoint = f"agent/invoke/{identifier}"

        response = self._client.make_request(method="GET", endpoint=endpoint)

        response_data = response.json()
        logger.debug(f"Get invocation response: {response_data}")

        # Response format with data in result field
        if response_data.get("ok") and "result" in response_data:
            result = response_data["result"]
            status = result.get("status", "Unknown")
            message = result.get("message", "")
            selected_agent = result.get("selectedAgent", "")

            # Generate action URL from port URLs in message if present
            # Necesarry to continue the interaction with the agent
            # Present them is the response for the agent to take action
            action_url = None
            if message:
                urls = re.findall(r'https://app\.getport\.io/self-serve[^\s<>"]*', message)
                if urls:
                    action_url = urls[0]

            if config.api_validation_enabled:
                return PortAgentResponse(
                    identifier=identifier,
                    status=status,
                    output=message,
                    error=None if status.lower() != "error" else message,
                    action_url=action_url,
                    selected_agent=selected_agent,
                    raw_output=response_data,
                )
            else:
                return PortAgentResponse.construct(
                    identifier=identifier,
                    status=status,
                    output=message,
                    error=None if status.lower() != "error" else message,
                    action_url=action_url,
                    selected_agent=selected_agent,
                )

        # If we don't have a result field, raise an error
        logger.error(f"Invalid response format: {response_data}")
        raise PortError(f"Invalid response format: {response_data}")
