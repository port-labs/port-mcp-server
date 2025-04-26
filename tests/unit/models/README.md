# MCP Server Port Models Test Suite

This directory contains unit tests for the MCP Server Port models. The test suite has been structured to provide clear separation of concerns and improve maintainability.

## File Structure

- **conftest.py**: Contains shared test models and fixtures used across all test files
- **test_base_models.py**: Tests for BaseModel implementations
- **test_tool.py**: Tests for Tool functionality
- **test_resource.py**: Tests for Resource functionality
- **test_resource_map.py**: Tests for ResourceMap
- **test_tool_map.py**: Tests for ToolMap
- **test_models.py**: (DEPRECATED) This file is now replaced by the split test files above

## Understanding `conftest.py`

In pytest, `conftest.py` is a special file that provides shared fixtures and setup code that can be used by multiple test files without explicit imports. Our `conftest.py` has two main purposes:

1. **Shared Test Model Classes**: These are test implementations of the actual models that are used across multiple test files. By placing them in `conftest.py`, we avoid duplicating code.

2. **Shared Fixtures**: Fixtures like `clean_resource_map` provide consistent test environments across different test files.

### Why this approach?

- **Reduced duplication**: Test models are defined once but used in many tests
- **Consistent testing**: All tests use the same model implementations
- **Easier maintenance**: Changes to test models only need to be made in one place
- **Cleaner test files**: Individual test files can focus on testing specific functionality

## Running Tests

To run all tests:

```bash
pytest tests/unit/models/
```

To run tests from a specific file:

```bash
pytest tests/unit/models/test_tool.py
``` 