import sys

import pytest

# Add src to path for imports
sys.path.append("src")

from pydantic import Field

from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.models.resources.resource import Resource
from src.models.resources.resource_map import ResourceMap
from src.models.tools.tool import Tool

#######################
# Test Model Classes  #
#######################
"""
These model classes provide test implementations of the actual models.
They're defined here so they can be imported by multiple test files.
"""


class TestBaseInputModel(BaseModel):
    __test__ = False
    """Test implementation of BaseModel for function inputs."""
    param1: str = Field(description="A string parameter")
    param2: int = Field(description="A numeric parameter")


class TestBaseOutputModel(BaseModel):
    __test__ = False
    """Test implementation of BaseModel for function outputs."""
    result: str = Field(description="A string result")


class TestBaseTool(Tool):
    __test__ = False
    """Test implementation of Tool."""

    def __init__(self):
        super().__init__(
            name="test_tool",
            description="A tool for testing",
            input_schema=TestBaseInputModel,
            output_schema=TestBaseOutputModel,
            function=self._function,
            annotations=Annotations(
                title="Test Tool",
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=True,
            ),
        )

    async def _function(self, args):
        """The actual function implementation that will be called by the tool."""
        return {"result": f"Called with {args['param1']}"}


class TestBaseResource(Resource):
    __test__ = False
    """Test implementation of Resource."""

    def __init__(self):
        super().__init__(
            name="test_resource",
            description="A resource for testing",
            uri="test://{param}",
            mimeType="text/plain",
            function=self.__call__,
        )

    async def __call__(self, param="default"):
        """The function that will be called when the resource is invoked."""
        return f"Resource content for {param}"


#######################
# Shared Fixtures     #
#######################
"""
These fixtures are available to all test files that import this conftest.py
"""


@pytest.fixture
def clean_resource_map():
    """
    Fixture that provides a clean ResourceMap instance for each test.

    This temporarily clears any registered resources in the ResourceMap singleton,
    and restores them after the test completes.

    Returns:
        ResourceMap: A clean ResourceMap instance with no resources registered.
    """
    resource_map = ResourceMap()
    # Store the original resources
    original_resources = resource_map.resources.copy()
    # Clear resources for the test
    resource_map.resources = {}

    # Yield the clean resource map to the test
    yield resource_map

    # Restore original resources after the test (cleanup)
    resource_map.resources = original_resources
