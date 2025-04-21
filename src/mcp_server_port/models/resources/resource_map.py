from dataclasses import field, dataclass
from typing import Callable
import mcp.types as types
from loguru import logger
from src.mcp_server_port.models.resources.resource import Resource
from src.mcp_server_port.models.common import Singleton
@dataclass
class ResourceMap(metaclass=Singleton):
    resources: dict[str, Resource] = field(default_factory=dict)
    
    def list_resources(self) -> list[types.Resource]:
        resources = [types.Resource(name=resource.name, description=resource.description, uri=resource.uri, mimeType=resource.mimeType) for resource in self.resources.values()]
        logger.info(f"Resource list: {resources}")
        return resources
    def get_resource(self, resource_name: str) -> Callable:
        resource = self.resources[resource_name]
        logger.info(f"Got resource: {resource_name}, {resource}")
        return resource.function
    def register_resource(self, resource: Resource) -> None:
        self.resources[resource.uri] = resource
        logger.info(f"Registered resource: {resource.name}, {resource.uri}")