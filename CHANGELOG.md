# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.4] - 2025-03-20

### Added
- New `get_blueprint` tool to retrieve detailed information about specific blueprints
- New `get_blueprints` tool to list all available blueprints
- Added corresponding Port resources for blueprint operations
- Improved code organization and structure through refactoring

## [0.0.3] - 2025-03-17

### Fixed
- Fixed compatibility issue with Port API changes in AI agent response handling

## [0.0.2] - 2025-03-06

### Changed
- Migrated to PyPort SDK for improved authentication and extensibility
- Removed token management functionality in favor of SDK handling

### Added
- Integration with PyPort SDK for better API interaction
- Simplified authentication process

## [0.0.1] - 2025-03-05

### Added
- Initial release of the Port MCP server
- Basic MCP server installation functionality
- AI agent interaction tool
- Token management system (later removed in 0.0.2) 