# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.14] - 2025-06-15

### Changed
- Upgraded `pyport` package to version 0.3.2. This resolves an existing bug where the client disconnects from Port after few hours and required a restart.


## [0.2.13] - 2025-06-15

### Changed
- Added the option to list actions as tools dynamically per user permissions

## [0.2.12] - 2025-06-09

### Changed
- Added `run_action` tool to run action
- Added `get_actions` tool to list actions 
- Added `track_action_run` tool to track action runs
- Added `get_action` tool to get action by identifier
- Fixed mypy errors

## [0.2.11] - 2025-06-04

### Changed
- Updated `pyport` dependency from `0.1.17` to `0.2.9`.

## [0.2.10] - 2025-06-04

### Changed
- Simplified AI agent response handling by removing conditional API validation.

## [0.1.8] - 2025-04-27

### Changed
- Upgraded Python from 3.10 to 3.13 in all GitHub workflows and project configuration
- Refactored codebase to use module-based architecture for better organization
- Replaced Dict/List with Python 3.9+ built-in types (dict/list)
- Updated Pydantic models to be compatible with Pydantic v2
- Enhanced configuration management with Pydantic-based validation
- Improved test structure with a more comprehensive approach
- Simplified CI/CD workflows with Makefile targets

### Added
- Added robust error handling and improved logging
- Implemented GitHub Actions workflows for CI
- Added linters (ruff, mypy) and formatters (black) via pyproject.toml
- Added CODEOWNERS file for better repository management
- Created dedicated model classes for Port tools

### Fixed
- Fixed line endings and whitespace issues
- Improved region configuration to properly handle US/EU values
- Fixed parameter validation in AI agent tool tests
- Enhanced error reporting with proper exception handling

## [0.1.7] - 2025-04-01

### Added
- New `get_scorecards` tool to list all scorecards
- New `get_scorecard` tool to retrieve information about a specific scorecard
- New `create_scorecard` tool to create new scorecards
- Added `PortScorecardClient` to handle scorecard interactions 

## [0.1.6] - 2025-03-23

### Added
- New `get_entities` tool to list all entities for a specific blueprint
- New `get_entity` tool to retrieve detailed information about specific entities
- Added entity models with support for properties and relations
- Added comprehensive test coverage for entity operations

### Changed
- Updated default prompt to include entity-related capabilities and workflow
- Improved team field typing in PortEntity model

## [0.1.5] - 2025-03-21

### Removed
- Removed individual blueprint endpoints (`port-blueprint://` and `port-blueprint-summary://`) as they weren't effectively accessible through eMCP, making them redundant
- Removed `_get_blueprint()` helper function as it's no longer needed

### Changed
- Simplified blueprint resources to focus on list-based endpoints only
- Improved documentation clarity for remaining blueprint endpoints
- Streamlined resource patterns documentation

## [0.1.4] - 2025-03-20

### Added
- New `get_blueprint` tool to retrieve detailed information about specific blueprints
- New `get_blueprints` tool to list all available blueprints
- Added corresponding Port resources for blueprint operations
- Improved code organization and structure through refactoring

## [0.1.3] - 2025-03-17

### Fixed
- Fixed compatibility issue with Port API changes in AI agent response handling

## [0.1.2] - 2025-03-06

### Changed
- Migrated to PyPort SDK for improved authentication and extensibility
- Removed token management functionality in favor of SDK handling

### Added
- Integration with PyPort SDK for better API interaction
- Simplified authentication process

## [0.1.1] - 2025-03-05

### Added
- Initial release of the Port MCP server
- Basic MCP server installation functionality
- AI agent interaction tool
- Token management system (later removed in 0.0.2)
