import json
import os
from typing import Any, Literal, cast

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

from src.utils import PortError, logger

# Load environment variables from .env file if it exists, but don't override existing env vars
load_dotenv(override=False)

REGION_TO_PORT_API_BASE = {"EU": "https://api.getport.io/v1", "US": "https://api.us.getport.io/v1"}


class McpServerConfig(BaseModel):
    port_client_id: str = Field(..., description="The client ID for the Port.io API")
    port_client_secret: str = Field(..., description="The client secret for the Port.io API")
    region: Literal["EU", "US"] = Field(default="EU", description="The region for the Port.io API")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="The log level for the server"
    )
    api_validation_enabled: bool | None = Field(default=False, description="Whether to enable API validation")
    log_path: Literal["/tmp/port-mcp.log"] = Field(default="/tmp/port-mcp.log", description="The path to the log file")

    def __str__(self) -> str:
        port_client_id = self.port_client_id
        port_client_secret = self.port_client_secret
        if port_client_id:
            start = port_client_id[:2]
            middle = "*" * (len(port_client_id) - 4)
            end = port_client_id[-2:]
            port_client_id = f"{start}{middle}{end}"
        if port_client_secret:
            start = port_client_secret[:2]
            middle = "*" * (len(port_client_secret) - 8)
            end = port_client_secret[-4:]
            port_client_secret = f"{start}{middle}{end}"
        config_dict = self.model_dump()
        config_dict["port_client_id"] = port_client_id
        config_dict["port_client_secret"] = port_client_secret
        return json.dumps(config_dict)

    @property
    def port_api_base(self) -> str:
        return REGION_TO_PORT_API_BASE[self.region]


def init_server_config(override: dict[str, Any] | None = None):
    global config
    if override is not None:
        config = McpServerConfig(
            port_client_id=override.get("port_client_id", ""),
            port_client_secret=override.get("port_client_secret", ""),
            region=override.get("region", "EU"),
            log_level=override.get("log_level", "ERROR"),
            api_validation_enabled=override.get("api_validation_enabled", "false") == "true",
        )
        return config
    try:
        client_id = os.environ.get("PORT_CLIENT_ID", "")
        client_secret = os.environ.get("PORT_CLIENT_SECRET", "")
        region = os.environ.get("PORT_REGION", "EU")
        log_level = os.environ.get("PORT_LOG_LEVEL", "ERROR").upper()
        api_validation_enabled = os.environ.get("PORT_API_VALIDATION_ENABLED", "False").lower() == "true"
        region = "US" if region.upper() == "US" else "EU"
        log_level = log_level.upper() or "ERROR"
        config = McpServerConfig(
            port_client_id=client_id,
            port_client_secret=client_secret,
            region=cast(Literal["EU", "US"], region),
            log_level=cast(Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], log_level),
            api_validation_enabled=api_validation_enabled,
        )
        return config
    except ValidationError as e:
        message = f"❌ Error initializing server config: {e.errors()}"
        logger.error(message)
        raise PortError(message) from e


config: McpServerConfig = init_server_config()
