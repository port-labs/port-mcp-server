import pytest
from .conftest import TestBaseTool

@pytest.mark.asyncio
async def test_base_tool_function():
    """Test that BaseTool.function correctly calls _function."""
    # Create a test tool
    tool = TestBaseTool()
    
    # Call the function method
    result = await tool.function({"param1": "test"})
    
    # Verify the result
    assert result == {"result": "Called with test"}


@pytest.mark.parametrize("test_input,is_valid,error_contains", [
    ({"param1": "test", "param2": 42}, True, None),  # Valid input
    ({"param2": 42}, False, "param1"),  # Missing required param
    ({"param1": "test", "param2": "not a number"}, False, "param2"),  # Wrong type
])
@pytest.mark.asyncio
async def test_base_tool_validation(test_input, is_valid, error_contains):
    """Test that BaseTool.validate_input correctly validates various inputs."""
    tool = TestBaseTool()
    
    if is_valid:
        validated = tool.validate_input(test_input)
        assert validated.model_dump() == test_input
    else:
        with pytest.raises(ValueError) as excinfo:
            tool.validate_input(test_input)
        assert error_contains in str(excinfo.value)


def test_tool_schema_properties():
    """Test that Tool correctly provides schema information."""
    tool = TestBaseTool()
    
    # Check inputSchema property
    input_schema = tool.inputSchema
    assert isinstance(input_schema, dict)
    assert "properties" in input_schema
    assert "param1" in input_schema["properties"]
    assert "param2" in input_schema["properties"]
    
    # Check outputSchema property
    output_schema = tool.outputSchema
    assert isinstance(output_schema, dict)
    assert "properties" in output_schema
    assert "result" in output_schema["properties"] 