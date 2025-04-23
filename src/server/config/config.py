import os
from typing import Literal, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv
from loguru import logger
# Load environment variables from .env file if it exists, but don't override existing env vars
load_dotenv(override=False)

REGION_TO_PORT_API_BASE = {
    "EU": "https://api.getport.io/v1",
    "US": "https://api.us.getport.io/v1"
}

class McpServerConfig(BaseModel):
    port_client_id: str = Field(..., description="The client ID for the Port.io API")
    port_client_secret: str = Field(..., description="The client secret for the Port.io API")
    region: Literal["EU", "US"] = Field(default="EU", description="The region for the Port.io API")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO", description="The log level for the server")

    @property
    def PORT_API_BASE(self) -> str:
        return REGION_TO_PORT_API_BASE[self.region]
    

    
def init_server_config(override :Dict[str, str] | None = None):
    if override is not None:
        global config
        config = McpServerConfig(**override)
    try:
        client_id = os.environ.get("PORT_CLIENT_ID")
        client_secret = os.environ.get("PORT_CLIENT_SECRET")
        region = os.environ.get("PORT_REGION") or "EU"
        log_level = os.environ.get("PORT_LOG_LEVEL") or "ERROR"
        config = McpServerConfig(port_client_id=client_id, port_client_secret=client_secret, region=region, log_level=log_level)
        return config
    except ValidationError as e:
        logger.error(e.errors())
        raise e.errors()

config: McpServerConfig = init_server_config()

