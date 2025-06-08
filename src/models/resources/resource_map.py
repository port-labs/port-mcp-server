from dataclasses import dataclass, field

import mcp.types as types

from src.models.resources.resource import Resource
from src.utils import logger


@dataclass
class ResourceMap:
    resources: dict[str, Resource] = field(default_factory=dict)

    def list_resources(self) -> list[types.Resource]:
        resources = [
            types.Resource(
                name=resource.name,
                description=resource.description,
                uri=types.AnyUrl(resource.uri),
                mimeType=resource.mime_type,
            )
            for resource in self.resources.values()
        ]
        logger.info(f"Resource list: {resources}")
        return resources

    def get_resource(self, resource_name: str) -> Resource:
        try:
            resource = self.resources[resource_name]
            logger.info(f"Got resource: {resource_name}, {resource}")
            return resource
        except KeyError:
            error_msg = f"Resource not found: {resource_name}"
            logger.error(error_msg)
            raise ValueError(error_msg) from None

    def register_resource(self, resource: Resource) -> None:
        if not resource.name:
            raise ValueError("Resource must have a name")

        if resource.name in self.resources:
            raise ValueError(f"Resource with name '{resource.name}' already registered")

        self.resources[resource.name] = resource
        logger.info(f"Registered resource: {resource.name}, {resource.uri}")
